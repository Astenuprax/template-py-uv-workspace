"""Golden eval — the audit tool against a table of repos with known-correct verdicts.

A lightweight, hermetic eval: each case pins the *exact* expected drift so a regression in
the audit logic (wrong conforms flag, miscounted missing) fails loudly against ground truth.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path

import pytest

from platform_core.tools import audit_structure

MakeRepo = Callable[[Iterable[str]], Path]  # mirrors the make_repo fixture in conftest.py

# (seeded entries, expected conforms, expected sorted-missing)
CASES = [
    pytest.param(["README.md", "pyproject.toml", "LICENSE"], True, [], id="full"),
    pytest.param(["README.md", "pyproject.toml"], False, ["LICENSE"], id="no-license"),
    pytest.param(["README.md"], False, ["LICENSE", "pyproject.toml"], id="readme-only"),
    pytest.param([], False, ["LICENSE", "README.md", "pyproject.toml"], id="empty"),
]


@pytest.mark.parametrize(("entries", "conforms", "missing"), CASES)
def test_audit_matches_golden(
    make_repo: MakeRepo, entries: list[str], conforms: bool, missing: list[str]
) -> None:
    report = audit_structure(str(make_repo(entries)))
    assert report.conforms is conforms
    assert sorted(report.missing) == missing
