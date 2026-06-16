"""Shared Repo-Analyser skill identifiers for runtime, Cursor install, and docs."""

CURSOR_SKILL_SLUGS: dict[str, str] = {
    "B1": "repo-inventory",
    "B2": "api-mapping",
    "B3": "test-discovery",
    "B4": "fastapi-greenfield",
    "B5": "node-greenfield",
    "B6": "rust-greenfield",
    "I1": "er-diagram",
    "I2": "flow-trace",
    "I3": "safe-change",
    "I4": "polyglot-pair",
    "I5": "dockerize",
    "I6": "bug-diagnosis",
    "A1": "worktree-plan",
    "A2": "worktree-execute",
    "A3": "fraud-system",
    "A4": "modernization",
    "A5": "code-review",
    "A6": "performance-tuning",
    "D1": "terraform",
    "D2": "compose-stack",
    "D3": "ci-pipeline",
    "D4": "kubernetes",
    "D5": "dev-bootstrap",
    "D6": "observability",
}

CURSOR_PREFIX = "repo-analyser"


def cursor_skill_name(task_id: str) -> str:
    slug = CURSOR_SKILL_SLUGS.get(task_id, task_id.lower())
    return f"{CURSOR_PREFIX}-{slug}"


def cursor_slash_command(task_id: str) -> str:
    return f"/{cursor_skill_name(task_id)}"
