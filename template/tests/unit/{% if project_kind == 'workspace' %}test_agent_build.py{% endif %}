"""Hermetic construction tests for the agent factory (no model call, no subprocess)."""

from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

from platform_core.agent import build_agent
from platform_core.settings import Settings


def test_build_agent_returns_agent_with_explicit_model() -> None:
    agent = build_agent(model=TestModel())
    assert isinstance(agent, Agent)


def test_build_agent_uses_settings_model_when_unspecified() -> None:
    settings = Settings(agent_model="anthropic:claude-sonnet-4-6")
    agent = build_agent(model=TestModel(), settings=settings)
    assert isinstance(agent, Agent)
