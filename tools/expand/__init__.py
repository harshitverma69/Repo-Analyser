"""Agent spec expansion package."""

from tools.expand.cli import main
from tools.expand.compiler import render_agent
from tools.expand.parser import _golden_schema

__all__ = ["_golden_schema", "main", "render_agent"]
