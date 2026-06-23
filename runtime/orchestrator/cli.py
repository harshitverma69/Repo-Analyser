"""CLI for skill DAG validation."""

from __future__ import annotations

import sys

from runtime.deterministic import canonical_json_dumps
from runtime.orchestrator import SkillOrchestrator


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Repo-Analyser skill orchestrator")
    parser.add_argument("--validate-dag", action="store_true", help="Validate skill dependency DAG")
    args = parser.parse_args(argv)

    if not args.validate_dag:
        print("Provide --validate-dag", file=sys.stderr)
        return 1

    orchestrator = SkillOrchestrator()
    report = orchestrator.validate_dag()
    print(canonical_json_dumps(report).rstrip())
    return 0 if report["dag_status"] == "VALID" else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
