"""Tests for YAML frontmatter support in agent spec parser."""

from __future__ import annotations

from pathlib import Path

from runtime.skill_parser import parse_agent_markdown, parse_agent_title, strip_frontmatter

ROOT = Path(__file__).resolve().parent.parent


def test_strip_frontmatter():
    text = "---\nname: foo\n---\n\n## Agent: Test (B1)\n"
    assert strip_frontmatter(text).startswith("## Agent:")


def test_strip_frontmatter_passthrough():
    text = "## Agent: Plain (B1)\n"
    assert strip_frontmatter(text) == text


def test_parse_agent_title_skips_frontmatter():
    text = "---\nname: x\n---\n\n## Agent: Repo Artifact Inventory Agent (B1)\n"
    match = parse_agent_title(strip_frontmatter(text))
    assert match is not None
    assert match.group(2) == "B1"


def test_parse_agent_markdown_expanded_b1():
    path = ROOT / "agents" / "basics" / "B1_repo_artifact_inventory_agent.md"
    agent = parse_agent_markdown(path)
    assert agent["skill_id"] == "B1"
    assert "repository_path" in agent["input_contract"]
    assert agent["output_contract"]["task_id"] == "B1"
    assert agent["canonical_output_file"] == "inventory_report.json"


def test_parse_agent_markdown_minimal_fixture(tmp_path: Path):
    agent_path = tmp_path / "B1_test_agent.md"
    agent_path.write_text(
        """---
name: cac-os-b1-test
description: test
---

# Agent: Test Agent (B1)

### Task ID
`B1`

### Capability Level
`B`

### Depends On
None

### Objective
Test objective

### Inputs
- repository_path (absolute string)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/B1/inventory_report.json`

```json
{"task_id": "B1", "files_scanned": 0}
```

### Validation
- ok

### Failure Conditions
- fail
""",
        encoding="utf-8",
    )
    agent = parse_agent_markdown(agent_path)
    assert agent["skill_id"] == "B1"
    assert agent["output_contract"]["files_scanned"] == 0
