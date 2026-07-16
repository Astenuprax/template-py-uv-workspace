---
id: ADR-0001
type: ADR
status: VERIFIED
gist: Adopt a single uv workspace (shared lock and venv) for the agent and its members over polyrepo or per-service venvs.
---

# ADR-0001: uv workspace over per-service dependency isolation

## Status

Accepted.

This record lives under `docs/adr/` because it is a durable Architecture Decision Record: a dated,
immutable account of one structural choice and the reasoning behind it. ADRs are co-located here so
the repo-structure-standard layout keeps decision history adjacent to — but separate from — runtime
code, and so the repo-hygiene frontmatter rule (every file under `docs/` carries enum-valid
frontmatter) applies uniformly.

## Context

The template ships a runnable AI/agentic example, not a library skeleton: a pydantic-ai
`governance-audit` agent (package `platform-core`). In this baseline the agent reaches its
`audit_structure` tool **in-process**; the `template-mcp-capability` overlay later adds a matched
`example-mcp-server` service (`services/`) that exposes the same tool over MCP/stdio. The agent and
that server are designed to evolve and run together as a matched pair.

Three packaging options were on the table:

- **Polyrepo** — agent and (future) MCP server in separate repositories, each with its own lock and
  release cadence.
- **Per-service virtual environments** — one repository, but a distinct `venv` and resolve per
  member, isolated dependency trees.
- **uv workspace** — one repository, one resolve, members declared under `packages/*` and
  `services/*`, sharing a single lock and environment.

The decision driver is that this is a portfolio-grade *template*: it must be cloned and run in one
command, present an obvious project shape, and keep its quality gate (ruff + pyright strict + pytest,
the `tests/test_structure.py` structure-lint, and `.pre-commit-config.yaml`) trivial to wire across
all members at once. Dependency divergence between the agent and its own MCP server is a non-goal —
they are designed as a matched pair.

## Decision

Adopt a **uv workspace**.

- A single workspace root declares members under `packages/*` (libraries such as `platform-core`)
  and `services/*` (deployable services, added by the mcp-capability overlay).
- All members share one `uv.lock` and one resolved virtual environment, materialised by
  `uv sync --all-packages`.
- Members remain **import- and build-isolated**: each is its own distribution with its own
  `pyproject.toml`, public API, and version; cross-member use goes through declared workspace
  dependencies, never via implicit path imports.
- The example agent is invoked through the workspace entry point, `uv run governance-agent .`.

The workspace gives import/build separation (clean package boundaries, independent buildable
artifacts) without giving — or attempting to give — dependency-resolution separation.

## Consequences

Pros:

- **One resolve.** A single `uv.lock` means every member sees one consistent, co-installable
  dependency set; there is no cross-service version skew to reconcile.
- **Atomic changes.** A change spanning the agent and a service is one commit, one review, one
  lockfile update — no multi-repo coordination or version-pinning dance.
- **Simple CI.** `uv sync --all-packages` builds the whole graph once; ruff, pyright (strict),
  pytest, the structure-lint gate, and the pre-commit hooks run across all members from one
  environment.
- **Obvious shape.** `packages/*` and `services/*` are self-documenting and align with the
  repo-structure-standard, so a reader orients immediately.

Cons:

- **Not true dependency isolation — stated explicitly.** Because every member resolves against one
  shared lock, two members cannot pin conflicting versions of the same transitive dependency; the
  resolver must satisfy all members simultaneously. If a future member genuinely required an
  incompatible dependency tree, the workspace could not express it and that member would have to move
  to its own repository or resolve. For an agent and its purpose-built MCP server this is an accepted,
  deliberate trade — they are released together by design — but it is a real constraint, not an
  oversight.

## Alternatives considered

- **Polyrepo.** Maximum isolation and independent release cadence, but it defeats the template's
  "clone and run in one command" goal, splits the quality gate and CI across repositories, and turns
  every agent-plus-server change into a cross-repo, version-pinned coordination problem. Rejected:
  the isolation it buys is value the matched agent/server pair does not need, at a cost the template
  cannot absorb.
- **Per-service venvs in one repo.** Keeps a single repository while granting each member its own
  resolve, so conflicting trees are expressible. Rejected: it reintroduces multi-environment
  management, multi-lock drift, and per-service gate wiring inside one repo — most of the polyrepo
  overhead with little of its benefit — for an isolation requirement that does not exist here.

---

Author: Phillip Anderson | Integrate-IT Australia
