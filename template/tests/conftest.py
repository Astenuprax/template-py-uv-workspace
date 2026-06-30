"""Shared fixtures: a factory that materialises throwaway repos for audit-tool tests."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path

import pytest

MakeRepo = Callable[[Iterable[str]], Path]


@pytest.fixture
def make_repo(tmp_path: Path) -> MakeRepo:
    """Return a factory that creates a directory seeded with the given entry names."""

    def _make(entries: Iterable[str]) -> Path:
        root = tmp_path / "repo"
        root.mkdir(exist_ok=True)
        for name in entries:
            (root / name).write_text("", encoding="utf-8")
        return root

    return _make
