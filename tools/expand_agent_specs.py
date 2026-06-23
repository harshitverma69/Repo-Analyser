"""Expand Repo-Analyser agent specs — backward-compatible entry point."""

from tools.expand import _golden_schema, main, render_agent

__all__ = ["_golden_schema", "main", "render_agent"]

if __name__ == "__main__":
    raise SystemExit(main())
