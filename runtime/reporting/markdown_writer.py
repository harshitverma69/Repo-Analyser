"""Write Markdown reports for skills and full runs."""

from __future__ import annotations

import json
from pathlib import Path

from runtime.reporting.loader import find_skill_json, load_skill_payload
from runtime.reporting.models import SKILL_TITLES
from runtime.reporting.renderer import render_report


def export_skill_markdown(skill_dir: Path, *, output_path: Path | None = None) -> Path:
    """Write output.md for a single skill directory. Returns the markdown path."""
    task_id, payload = load_skill_payload(skill_dir)
    if not payload:
        raise FileNotFoundError(f"No JSON output found in {skill_dir}")

    md_path = output_path or (skill_dir / "output.md")
    md_path.write_text(render_report(payload, task_id=task_id), encoding="utf-8")
    return md_path


def export_run_markdown(run_dir: Path) -> list[Path]:
    """Write output.md for every skill subdirectory that has JSON output."""
    written: list[Path] = []
    if not run_dir.is_dir():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    for skill_dir in sorted(run_dir.iterdir(), key=lambda path: path.name):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        if skill_dir.name == "manifest.json":
            continue
        if find_skill_json(skill_dir) is None:
            continue
        written.append(export_skill_markdown(skill_dir))

    index_path = run_dir / "REPORT.md"
    index_path.write_text(_render_run_index(run_dir, written), encoding="utf-8")
    written.insert(0, index_path)
    return written


def _render_run_index(run_dir: Path, skill_reports: list[Path]) -> str:
    manifest_path = run_dir / "manifest.json"
    repo = ""
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        repo = manifest.get("repository_path", "")

    lines = [
        f"# Repo-Analyser Run Report — `{run_dir.name}`",
        "",
    ]
    if repo:
        lines.extend([f"**Repository:** `{repo}`", ""])

    lines.extend(["## Skills", ""])
    for report_path in skill_reports:
        if report_path.name == "REPORT.md":
            continue
        skill_id = report_path.parent.name
        title = SKILL_TITLES.get(skill_id, skill_id)
        rel = report_path.relative_to(run_dir).as_posix()
        lines.append(f"- [{skill_id} — {title}]({rel})")
    lines.append("")
    return "\n".join(lines)
