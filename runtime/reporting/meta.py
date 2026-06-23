"""Summary and metadata sections for skill reports."""

from __future__ import annotations

from runtime.reporting.formatters import table


def meta_section(payload: dict) -> str:
    rows: list[tuple[str, str]] = []
    for key in ("level", "generated_at", "scan_complete", "files_scanned", "repository_path"):
        if key in payload and payload[key] is not None:
            rows.append((key.replace("_", " ").title(), str(payload[key])))

    if payload.get("warnings"):
        rows.append(("Warnings", str(len(payload["warnings"]))))
    if payload.get("limitations"):
        rows.append(("Limitations", str(len(payload["limitations"]))))

    lines = ["## Summary", ""]
    if rows:
        lines.extend(table(["Field", "Value"], rows))
        lines.append("")

    if payload.get("warnings"):
        lines.extend(["### Warnings", ""])
        for warning in payload["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")

    if payload.get("limitations"):
        lines.extend(["### Known Limitations", ""])
        for item in payload["limitations"]:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines).rstrip()
