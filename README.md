# template-py-uv-workspace

The **Python uv-workspace stack overlay** of the `template-*` family — a [Copier](https://copier.readthedocs.io)
template that composes **on top of** [`template-governance-base`](https://github.com/Astenuprax/template-governance-base)
to materialise the *AI-monorepo (Python, uv workspace)* archetype from `repo-structure-standard`.

The base contributes the stack-agnostic governance kernel (furniture, licence, the universal
pre-commit gate). This overlay adds, on top:

- a uv **virtual workspace** (`pyproject.toml` with `[tool.uv.workspace]`, one `uv.lock`, one `.venv`);
- an example typed `src`-layout member, `packages/platform-core/` (a bare pydantic-ai agent — **no MCP**;
  the MCP capability is the separate `template-mcp-capability` overlay);
- the **structure-lint** (`tests/test_structure.py`) — the archetype's layout rules as failing tests,
  with the `[tool.structure_lint]` data + a two-tier shrink-floor;
- the `ruff` + `pyright (strict)` + `pytest` toolchain, wired into the base's pre-commit gate.

## Use

```bash
# 1. Render the governance base, then this overlay on top (apply order matters).
#    --overwrite lets the overlay replace the base's seed files; without it copier
#    conflict-prompts and the default (keep-existing) leaves a half-composed repo:
uvx copier copy --overwrite gh:Astenuprax/template-governance-base ./my-repo
uvx copier copy --overwrite gh:Astenuprax/template-py-uv-workspace  ./my-repo
# 2. Resolve the workspace lock (uv.lock is intentionally not templated):
cd my-repo && uv lock && uv sync --all-packages
# 3. Initialise git (copier does not), then activate the gate:
git init && uvx pre-commit install
```

Pull later stack changes independently of the base with
`uvx copier update -a .copier-answers.python.yml` (3-way merge; your code seeds are preserved).

## Apply order

`template-governance-base` → **`template-py-uv-workspace`** → `template-mcp-capability` (optional).

---

Author: Phillip Anderson | Integrate-IT Australia. License: Apache-2.0 (see `LICENSE`).
