# platform-core

Shared runtime for the python uv-workspace template: a typed
[pydantic-ai](https://ai.pydantic.dev) governance-audit agent, its tool(s), settings, and tracing.

The agent audits a repository (or config) against a required-structure standard and reports drift —
a small, deterministic, self-demonstrating example of an agent-plus-tool architecture. The tool runs
in-process; the `template-mcp-capability` overlay re-wires the same tool through an MCP server.

## Install

```console
uv add platform-core            # or: pip install platform-core
```

Ships `py.typed` — fully type-checked, strict-mode clean for downstream consumers.

## Use

```python
from platform_core.tools import audit_structure

report = audit_structure(".")
print(report.conforms, report.missing)
```

The packaged console script runs the agent end-to-end (needs `ANTHROPIC_API_KEY`; without it, it
falls back to a direct tool call):

```console
governance-agent
```

## What's inside

| Module | Responsibility |
|---|---|
| `agent.py` | the pydantic-ai agent, wired to its tool in-process (MCP-free) |
| `tools.py` | `audit_structure` + the `AuditReport` contract |
| `settings.py` | pydantic-settings config (reads `.env`) |
| `tracing.py` | no-op-safe OpenTelemetry/logfire setup |

Licensed Apache-2.0. See the workspace `README.md` for architecture and contribution guidance.
