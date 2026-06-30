"""The runnable governance-audit agent (pydantic-ai), wired directly to its tool.

This is the MCP-FREE variant shipped by the python-stack overlay: the agent reaches
``audit_structure`` as a plain in-process pydantic-ai tool, so the whole stack renders and
runs green with no ``services/`` and no MCP dependency in the resolved closure. The
mcp-capability overlay (``template-mcp-capability``) re-wires this same tool through an MCP
server over stdio.

The ``main`` entrypoint runs the full LLM agent when ``ANTHROPIC_API_KEY`` is set, and
otherwise falls back to a direct tool call so the example is demonstrable with no credentials.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from pydantic_ai import Agent

from platform_core.settings import Settings, load_settings
from platform_core.tools import audit_structure
from platform_core.tracing import configure_tracing

if TYPE_CHECKING:
    from pydantic_ai.models import Model

SYSTEM_PROMPT = (
    "You are a governance-assurance assistant. Use the audit_structure tool to "
    "check a directory against the structure standard, then report any drift "
    "(missing required files) concisely."
)


def build_agent(model: Model | str | None = None, settings: Settings | None = None) -> Agent:
    """Build the agent with the audit tool. Pass ``model`` (e.g. a TestModel) to override."""
    settings = settings or load_settings()
    return Agent(
        model or settings.agent_model,
        tools=[audit_structure],
        system_prompt=SYSTEM_PROMPT,
    )


def main() -> None:
    """Run the agent against a target directory (defaults to cwd)."""
    configure_tracing()
    settings = load_settings()
    target = sys.argv[1] if len(sys.argv) > 1 else "."

    if settings.anthropic_api_key:
        agent = build_agent(settings=settings)
        result = agent.run_sync(f"Audit the directory {target!r} and report any structure drift.")
        print(result.output)
    else:
        report = audit_structure(target)
        print("[no ANTHROPIC_API_KEY -> direct tool call]")
        print(report.model_dump())


if __name__ == "__main__":
    main()
