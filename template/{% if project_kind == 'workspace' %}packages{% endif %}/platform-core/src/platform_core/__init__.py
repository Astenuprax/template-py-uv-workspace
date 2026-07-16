"""platform-core: the governance-audit agent runtime (agent, tool, settings, tracing).

Only the lightweight tool API is re-exported here so importing it does not pull in the
agent's model stack. Import the agent explicitly: ``from platform_core.agent import build_agent``.
"""

from platform_core.tools import AuditReport, audit_structure

__all__ = ["AuditReport", "audit_structure"]
