"""Behaviour tests for the audit tool — the one real, deterministic, verifiable unit."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path

from platform_core.tools import DEFAULT_REQUIRED, AuditReport, audit_structure

# Mirrors the `make_repo` fixture's return type in conftest.py. Declared locally because
# tests/ is not an importable package and a shared tests/_types.py would trip the
# structure-lint (non-test .py under tests/).
MakeRepo = Callable[[Iterable[str]], Path]


def test_conforms_when_all_required_present(make_repo: MakeRepo) -> None:
    repo = make_repo(DEFAULT_REQUIRED)
    report = audit_structure(str(repo))
    assert isinstance(report, AuditReport)
    assert report.conforms is True
    assert report.missing == []
    assert sorted(report.present) == sorted(DEFAULT_REQUIRED)


def test_reports_drift_when_required_missing(make_repo: MakeRepo) -> None:
    repo = make_repo(["README.md", "pyproject.toml"])  # LICENSE absent
    report = audit_structure(str(repo))
    assert report.conforms is False
    assert report.missing == ["LICENSE"]
    assert set(report.present) == {"README.md", "pyproject.toml"}


def test_empty_dir_is_all_drift(make_repo: MakeRepo) -> None:
    repo = make_repo([])
    report = audit_structure(str(repo))
    assert report.conforms is False
    assert sorted(report.missing) == sorted(DEFAULT_REQUIRED)
    assert report.present == []


def test_custom_required_set(make_repo: MakeRepo) -> None:
    repo = make_repo(["a.txt"])
    report = audit_structure(str(repo), required=("a.txt", "b.txt"))
    assert report.conforms is False
    assert report.present == ["a.txt"]
    assert report.missing == ["b.txt"]


def test_target_is_echoed(tmp_path: Path) -> None:
    report = audit_structure(str(tmp_path))
    assert report.target == str(tmp_path)
