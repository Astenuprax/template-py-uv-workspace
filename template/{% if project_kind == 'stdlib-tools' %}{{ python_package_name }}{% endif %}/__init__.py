"""{{ project_name }} — stdlib-only tools package.

Flat root package (not a `packages/` workspace member): no `[build-system]`, no editable
install. Tools run in place via `python -m {{ python_package_name }}.<tool>` from a bare
clone with the working directory at the repo root (so this package is importable off
`sys.path[0]` without installation).

Stdlib-only contract: every top-level import in this package (and its submodules) must
resolve to `sys.stdlib_module_names` or to `{{ python_package_name }}` itself — see
`tests/test_structure.py`'s stdlib-only-import guard.
"""

from __future__ import annotations
