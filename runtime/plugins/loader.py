"""Auto-discover skill plugins from registry and builtins."""

from __future__ import annotations

from pathlib import Path

from runtime.models import RunContext, SkillResult, SkillSpec
from runtime.orchestrator.executor import SkillExecutor
from runtime.orchestrator.planner import discover_skills, load_registry
from runtime.plugins.base import BaseSkillPlugin
from runtime.plugins.registry import PluginRegistry

ROOT = Path(__file__).resolve().parent.parent.parent
CORE_REGISTRY_PATH = ROOT / "core" / "skill_registry.json"


class GoldenReplayPlugin(BaseSkillPlugin):
    """Deterministic golden-replay plugin for a single skill."""

    def __init__(self, skill_id: str, spec: SkillSpec):
        self.id = skill_id
        self.version = "1.0.0"
        self._spec = spec

    def execute(self, context: RunContext) -> SkillResult:
        skills = discover_skills()
        skill = skills[self.id]
        executor = SkillExecutor(context)
        return executor.run_skill(skill)


def load_plugins(registry_path: Path = CORE_REGISTRY_PATH) -> PluginRegistry:
    registry = PluginRegistry()
    skill_registry = load_registry(registry_path)
    skills = discover_skills()

    for skill_id, meta in sorted(skill_registry.get("skills", {}).items()):
        spec = SkillSpec.from_registry_entry(skill_id, meta)
        if skill_id in skills:
            registry.register(GoldenReplayPlugin(skill_id, spec))

    return registry


def discover_plugins(registry_path: Path | None = None) -> PluginRegistry:
    """Public entry: auto-discover plugins from skills package + registry."""
    return load_plugins(registry_path or CORE_REGISTRY_PATH)
