"""Load skill JSON payloads from run directories."""

from __future__ import annotations

import json
from pathlib import Path


def find_skill_json(skill_dir: Path) -> Path | None:
    """Locate the JSON payload for a skill output directory."""
    if not skill_dir.is_dir():
        return None
    preferred = skill_dir / "output.json"
    if preferred.is_file():
        return preferred
    json_files = sorted(skill_dir.glob("*.json"))
    return json_files[0] if json_files else None


def load_skill_payload(skill_dir: Path) -> tuple[str | None, dict]:
    json_path = find_skill_json(skill_dir)
    if json_path is None:
        return None, {}
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    task_id = payload.get("task_id") or skill_dir.name
    return task_id, payload
