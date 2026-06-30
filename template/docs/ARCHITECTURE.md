---
id: ARCH-001
type: REFERENCE
status: VERIFIED
gist: How this uv-workspace template wires the platform-core pydantic-ai governance-audit agent (in-process tool, MCP-free) into one import-isolated, gate-enforced repository.
---

# Architecture

This repository is a portfolio-grade template for AI/agentic Python projects, built on the **python
uv-workspace** stack overlay composed onto `template-governance-base`. Its worked example is a
**governance-audit agent** (package `platform-core`, built on [pydantic-ai](https://ai.pydantic.dev))
that reaches a single tool **in-process** — the MCP-free baseline. The `template-mcp-capability`
overlay re-wires the same tool through an MCP server over stdio and adds the `services/` member.

Repository layout follows the **repo-structure-standard**; mechanical hygiene follows
**repo-hygiene**; coding and skeleton conventions follow **governance-standards**. Those standards
are referenced by name throughout and are not restated here.

---

## 1. The uv workspace

The repo is a single [uv](https://docs.astral.sh/uv/) workspace: one root `pyproject.toml` declares
`[tool.uv.workspace]` members, and every member resolves against **one shared lockfile** (`uv.lock`)
into **one shared virtual environment** (`.venv`).

```
<repo>/
  pyproject.toml            # workspace root: members, dev deps, tool config, [tool.structure_lint]
  uv.lock                   # single resolved lock for the whole workspace (run `uv lock` post-render)
  packages/
    platform-core/          # pydantic-ai governance-audit agent (in-process tool)
  services/                 # deployable members (none in this baseline; added by mcp-capability)
  tests/
    test_structure.py       # structure-lint gate (per repo-structure-standard)
    unit/                   # offline behaviour + golden eval
  docs/
    ARCHITECTURE.md         # this file
  .pre-commit-config.yaml   # base governance hooks + ruff + pyright(strict) + structure-lint
  LICENSE                   # Apache-2.0, verbatim
  NOTICE                    # attribution
```

**Why a uv workspace.** A workspace gives one resolution graph, so members can never disagree on a
shared dependency's version. `uv sync --all-packages` installs every member editable in one pass;
`uv run governance-agent .` launches the agent entry point without per-package environment juggling.
New members are added by dropping a package under `packages/` (or a service under `services/`) and
listing it in the workspace `members` glob — no new lock, no new venv.

---

## 2. The `platform-core` agent runtime

`platform-core` is the agent package. Its runtime is split into single-responsibility modules so
configuration, behaviour, instrumentation, and tool logic stay independently testable.

| Module | Responsibility |
|---|---|
| `settings.py` | Typed configuration via `pydantic-settings` — model id, optional API key. Loaded from the environment; no literals scattered through the code. |
| `tracing.py` | Best-effort OpenTelemetry / logfire setup (no-op safe when logfire is absent). |
| `tools.py` | The `audit_structure` tool + the typed `AuditReport` result contract — deterministic and dependency-free. |
| `agent.py` | Constructs the pydantic-ai `Agent`, registers `audit_structure` as an in-process tool, and exposes the `governance-agent` console entry point. |

`agent.py` is the composition root: it reads `settings.py`, initialises `tracing.py`, builds the
agent with the tool from `tools.py`, and runs it against a target directory
(`uv run governance-agent .`). With no `ANTHROPIC_API_KEY` set, the entry point falls back to a
direct tool call so the example runs with no credentials.

---

## 3. Agent <-> tool data flow

```
            uv run governance-agent .
                      |
                      v
   +--------------------------------------+
   |  platform-core (agent.py)            |
   |  Agent(model, tools=[audit_structure])|
   +--------------------------------------+
            |                  ^
            | tool call:       | AuditReport (drift)
            | audit_structure  |
            v                  |
   +--------------------------------------+
   |  tools.audit_structure(path) -> drift|
   +--------------------------------------+
            |                  ^
            | reads files      | structural findings
            v                  |
        target directory (the repo under audit)
```

1. The agent run starts.
2. The model decides to call `audit_structure` with the target path — an in-process Python call (no
   subprocess, no transport boundary).
3. The tool walks the target directory, compares it against a minimal required-structure set, and
   returns the discovered drift.
4. pydantic-ai validates the findings into a typed **`AuditReport`** — the agent's result contract.

The `template-mcp-capability` overlay replaces step 2's in-process call with an MCP-over-stdio
round-trip to an `example-mcp-server` service, without changing the `audit_structure` contract.

---

## 4. Isolation model

The workspace shares **one lockfile and one venv**, so isolation here is **import + build isolation,
not dependency isolation**:

- **Import isolation** — each member is its own importable distribution with its own `[project]`
  table, entry points, and public surface.
- **Build isolation** — each member builds and versions independently and could be published alone.
- **Shared resolution (by design)** — because all members resolve against one lock, they cannot
  drift to conflicting versions of a shared dependency. The trade-off (no per-member dependency
  isolation) is recorded in `docs/adr/0001-uv-workspace.md`.

---

## 5. Test and gate layers

Quality is enforced in layers, all run from the shared venv and wired into `.pre-commit-config.yaml`:

| Layer | Tool | Checks |
|---|---|---|
| Universal governance | `tools/governance_checks.py` (base) | Actions SHA-pinned, LICENSE verbatim, root-MD allowlist, docs frontmatter. |
| Lint / format | `ruff` | Style, import order, lint + security (bandit) rules. |
| Types | `pyright` (strict) | Full strict static typing — typed settings and the `AuditReport` contract. |
| Unit / behaviour | `pytest` | Agent construction + the `audit_structure` tool, including a golden eval. |
| Structure lint | `tests/test_structure.py` | Asserts the repo matches **repo-structure-standard** + **repo-hygiene** — the same expectations the agent itself audits. |

Local runs and CI invoke the same gate. The structure-lint is intentionally recursive: the template
enforces on itself the standard its example agent is built to detect.

---

*Author: Phillip Anderson | Integrate-IT Australia. Licensed under Apache-2.0 (see `LICENSE`;
attribution in `NOTICE`).*
