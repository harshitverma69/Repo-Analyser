"""Convert skill JSON payloads to Markdown reports."""

from __future__ import annotations

from runtime.reporting.handlers import TASK_HANDLERS, render_generic
from runtime.reporting.meta import meta_section
from runtime.reporting.models import SKILL_TITLES


def render_report(payload: dict, *, task_id: str | None = None) -> str:
    """Convert a skill JSON payload to Markdown."""
    tid = task_id or str(payload.get("task_id", "unknown"))
    title = SKILL_TITLES.get(tid, tid)
    lines: list[str] = [
        f"# {tid} — {title}",
        "",
        meta_section(payload).rstrip(),
        "",
    ]

    handler = TASK_HANDLERS.get(tid, render_generic)
    body = handler(payload)
    if body.strip():
        lines.append(body.rstrip())
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
