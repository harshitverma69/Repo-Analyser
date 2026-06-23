"""CLI for expanding agent specs."""

from __future__ import annotations

from tools.expand.compiler import render_agent
from tools.expand.parser import _agent_path
from tools.expand.template_engine import REGISTRY


def main() -> int:
    updated: list[str] = []
    for task_id in sorted(REGISTRY["skills"].keys(), key=lambda t: (t[0], int(t[1:]))):
        path = _agent_path(task_id)
        if not path.is_file():
            print(f"SKIP {task_id}: missing {path}", file=__import__("sys").stderr)
            continue
        content = render_agent(task_id)
        path.write_text(content + "\n", encoding="utf-8")
        updated.append(task_id)
    print(f"Expanded {len(updated)} agent specs: {', '.join(updated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
