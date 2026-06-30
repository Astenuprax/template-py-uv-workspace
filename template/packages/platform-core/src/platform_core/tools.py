"""The agent's governance-audit tool.

A generic, self-demonstrating governance-assurance check: audit a directory
against a minimal structure standard and report drift (required entries that
are missing). No client/vendor coupling — the "standard" is just a tuple of
required entry names, so the same logic dogfoods the repo-structure-conformance
theme without embedding any private rule set.
"""

from pathlib import Path

from pydantic import BaseModel, Field

#: The minimal structure standard this demonstrator audits against.
DEFAULT_REQUIRED: tuple[str, ...] = ("README.md", "pyproject.toml", "LICENSE")


class AuditReport(BaseModel):
    """Structured result of a structure audit (typed output — showcases type rigor)."""

    target: str = Field(description="The audited directory path.")
    conforms: bool = Field(description="True when no required entry is missing.")
    present: list[str] = Field(default_factory=list, description="Required entries that exist.")
    missing: list[str] = Field(
        default_factory=list, description="Required entries missing (drift)."
    )


def audit_structure(path: str, required: tuple[str, ...] = DEFAULT_REQUIRED) -> AuditReport:
    """Audit ``path`` against ``required`` and report which entries are missing.

    Deterministic and dependency-free, so it is directly unit-testable and gives
    the agent tool a verifiable, assertable output.
    """
    base = Path(path)
    present = [name for name in required if (base / name).exists()]
    missing = [name for name in required if name not in present]
    return AuditReport(
        target=str(base),
        conforms=not missing,
        present=present,
        missing=missing,
    )
