"""Deterministic skill DAG orchestrator — backward-compatible module."""

from runtime.orchestrator import ExecutionPlan, SkillOrchestrator
from runtime.orchestrator.cli import main

__all__ = ["ExecutionPlan", "SkillOrchestrator", "main"]

if __name__ == "__main__":
    import sys

    sys.exit(main())
