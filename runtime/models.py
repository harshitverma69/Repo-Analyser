"""Typed domain models for skill execution and reporting."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from runtime.skill_parser import SkillDefinition


@dataclass(frozen=True)
class SkillDependency:
    skill_id: str
    depends_on: str

    def to_dict(self) -> dict[str, str]:
        return {"skill_id": self.skill_id, "depends_on": self.depends_on}


@dataclass
class SkillSpec:
    """Registry-facing skill specification."""

    skill_id: str
    name: str
    level: str
    level_code: str
    depends_on: list[str] = field(default_factory=list)
    input_contract: dict[str, Any] = field(default_factory=dict)
    output_contract: dict[str, Any] = field(default_factory=dict)
    source_path: str = ""
    output_file: str = "output.json"

    @classmethod
    def from_definition(cls, definition: SkillDefinition, output_file: str = "output.json") -> SkillSpec:
        return cls(
            skill_id=definition.skill_id,
            name=definition.name,
            level=definition.level,
            level_code=definition.level_code,
            depends_on=list(definition.depends_on),
            input_contract=dict(definition.input_contract),
            output_contract=dict(definition.output_contract),
            source_path=definition.source_path,
            output_file=output_file,
        )

    @classmethod
    def from_registry_entry(cls, skill_id: str, meta: dict[str, Any]) -> SkillSpec:
        return cls(
            skill_id=skill_id,
            name=str(meta.get("name", skill_id)),
            level=str(meta.get("level", "")),
            level_code=str(meta.get("level_code", skill_id[0])),
            depends_on=list(meta.get("depends_on", [])),
            input_contract=dict(meta.get("input_contract", {})),
            output_contract=dict(meta.get("output_contract", {})),
            source_path=str(meta.get("path", "")),
            output_file=str(meta.get("output_file", "output.json")),
        )


@dataclass
class RunContext:
    """Inputs and paths for a single pipeline run."""

    run_id: str
    run_dir: Path
    golden_dir: Path
    registry_path: Path
    inputs: dict[str, Any] = field(default_factory=dict)
    continue_on_failure: bool = True

    @property
    def repository_path(self) -> str:
        return str(self.inputs.get("repository_path", ""))


@dataclass
class SkillResult:
    """Outcome of executing one skill."""

    skill_id: str
    status: str
    output_path: str
    started_at: str
    completed_at: str
    steps_executed: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "status": self.status,
            "output_path": self.output_path,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "steps_executed": self.steps_executed,
            "errors": sorted(self.errors),
        }

    @classmethod
    def from_legacy(cls, legacy: Any) -> SkillResult:
        return cls(
            skill_id=legacy.skill_id,
            status=legacy.status,
            output_path=legacy.output_path,
            started_at=legacy.started_at,
            completed_at=legacy.completed_at,
            steps_executed=list(legacy.steps_executed),
            errors=list(legacy.errors),
        )


@dataclass
class ExecutionReport:
    """Summary of a full pipeline or partial run."""

    run_id: str
    status: str
    completed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    execution_log: str = ""
    final_report: str = ""
    skills_requested: list[str] = field(default_factory=list)
    total_skills: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "completed": self.completed,
            "failed": self.failed,
            "execution_log": self.execution_log,
            "final_report": self.final_report,
            "skills_requested": self.skills_requested,
            "total_skills": self.total_skills,
            "completed_count": len(self.completed),
            "failed_count": len(self.failed),
        }


@dataclass
class ExecutionPlanModel:
    """Typed execution plan (mirrors orchestrator ExecutionPlan)."""

    run_id: str
    requested: list[str]
    execution_order: list[str]
    parallel_waves: list[list[str]]
    skill_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "requested": self.requested,
            "execution_order": self.execution_order,
            "parallel_waves": self.parallel_waves,
            "skill_ids": self.skill_ids,
        }
