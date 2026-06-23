"""Skill orchestration facade — backward-compatible public API."""

from __future__ import annotations

from runtime.orchestrator import dependency_resolver, planner
from runtime.orchestrator.planner import ExecutionPlan, discover_skills, load_registry

__all__ = ["ExecutionPlan", "SkillOrchestrator"]


class SkillOrchestrator:
    """Discover skills, validate DAG, and build execution plans."""

    def __init__(self, skills_root=None, registry_path=None):
        self.skills_root = skills_root or planner.SKILLS_ROOT
        self.registry_path = registry_path or planner.CORE_REGISTRY_PATH
        self._skills: dict = {}
        self._registry: dict = {}

    def load_registry(self) -> dict:
        self._registry = load_registry(self.registry_path)
        return self._registry

    def discover_skills(self) -> dict:
        self._skills = discover_skills(self.skills_root)
        return self._skills

    def get_skill(self, skill_id: str):
        if not self._skills:
            self.discover_skills()
        skill = self._skills.get(skill_id.upper())
        if skill is None:
            raise KeyError(f"Unknown skill: {skill_id}")
        return skill

    def dependency_graph(self, skill_ids: list[str] | None = None) -> dict[str, list[str]]:
        if not self._registry:
            self.load_registry()
        return planner.dependency_graph(self._registry, skill_ids)

    def collect_transitive(self, requested: list[str], graph: dict[str, list[str]]) -> set[str]:
        return dependency_resolver.collect_transitive(requested, graph)

    def detect_cycle(self, graph: dict[str, list[str]]) -> str | None:
        return dependency_resolver.detect_cycle(graph)

    def detect_cycles(self, graph: dict[str, list[str]]) -> list[str]:
        return dependency_resolver.detect_cycles(graph)

    def find_missing_dependencies(self, graph: dict[str, list[str]]) -> list[dict[str, str]]:
        return dependency_resolver.find_missing_dependencies(graph)

    def find_orphan_skills(self, graph: dict[str, list[str]]) -> list[str]:
        return dependency_resolver.find_orphan_skills(graph)

    def validate_dag(self) -> dict:
        if not self._registry:
            self.load_registry()
        return planner.validate_dag(self._registry)

    def topological_sort(self, requested: list[str]) -> list[str]:
        graph = self.dependency_graph()
        return dependency_resolver.topological_sort(requested, graph)

    def parallel_waves(self, execution_order: list[str]) -> list[list[str]]:
        graph = self.dependency_graph()
        return dependency_resolver.parallel_waves(execution_order, graph)

    def skills_for_domain(self, domain: str) -> list[str]:
        if not self._registry:
            self.load_registry()
        return planner.skills_for_domain(self._registry, domain)

    def full_pipeline_skills(self) -> list[str]:
        if not self._registry:
            self.load_registry()
        return planner.full_pipeline_skills(self._registry)

    def build_plan(
        self,
        run_id: str,
        skill_ids: list[str] | None = None,
        domain: str | None = None,
        full_pipeline: bool = False,
    ) -> ExecutionPlan:
        if not self._registry:
            self.load_registry()
        if not self._skills:
            self.discover_skills()
        return planner.build_plan(
            run_id,
            self._registry,
            self._skills,
            skill_ids=skill_ids,
            domain=domain,
            full_pipeline=full_pipeline,
        )
