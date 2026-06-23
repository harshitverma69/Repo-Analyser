"""Plugin protocol and base types for skill execution."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from runtime.models import RunContext, SkillResult


@runtime_checkable
class SkillPlugin(Protocol):
    id: str
    version: str

    def execute(self, context: RunContext) -> SkillResult:
        """Run the skill against the given context."""
        ...


class BaseSkillPlugin:
    """Optional base class for concrete plugins."""

    id: str = "base"
    version: str = "1.0.0"

    def execute(self, context: RunContext) -> SkillResult:
        raise NotImplementedError
