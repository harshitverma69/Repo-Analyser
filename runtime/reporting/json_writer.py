"""Write canonical JSON reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime.deterministic import canonical_json_dumps


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json_dumps(payload), encoding="utf-8")
    return path
