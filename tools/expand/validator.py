"""Validate task IDs and agent paths before expansion."""

from __future__ import annotations

from tools.expand.parser import _agent_path
from tools.expand.template_engine import REGISTRY


def validate_task_id(task_id: str) -> list[str]:
    errors: list[str] = []
    if task_id not in REGISTRY.get("skills", {}):
        errors.append(f"Unknown task: {task_id}")
    path = _agent_path(task_id)
    if not path.is_file():
        errors.append(f"Missing agent spec: {path}")
    return errors


def validate_all_tasks() -> dict[str, list[str]]:
    return {task_id: validate_task_id(task_id) for task_id in sorted(REGISTRY["skills"].keys())}
