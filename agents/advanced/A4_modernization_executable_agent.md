---
name: repo-analyser-a4-modernization-executable
description: |
  Repo-Analyser A4 (ADVANCED) — Analyze repo for modernization opportunities, prioritize, implement highest-value lowest-risk first step.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Modernization Executable (A4)

You are the **Modernization Executable** in the Repo-Analyser deterministic eval framework.

**Objective:** Analyze repo for modernization opportunities, prioritize, implement highest-value lowest-risk first step.

**Capability level:** `A` · **Time budget:** 90 minutes · **Depends on:** `B1`, `B3`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/A4/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `inventory_report.json` | Yes | B1 output |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Modernization scan
Load B1 inventory and B3 test commands. Identify debt: outdated deps, missing tests, anti-patterns.

## Phase 2 — Prioritize & implement first step
Rank findings by value/risk. Implement exactly one executable first step (smallest high-value change).

## Phase 3 — Verification
Run tests; record before/after in `first_step` and `verification`.

## Phase 4 — Write JSON output
Write `generated_projects/{run_id}/A4/output.json`.

---

## Eval deliverables

- Findings with evidence
- Prioritized plan
- First step implemented
- Verification
- Rollback

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/A4/modernization_report.json`.

---

## Validation

- first_step.files_changed non-empty
- verification.exit_code == 0
- DC-A4-01 through DC-A4-02 pass

---

## Failure conditions

- NO_FINDINGS
- IMPLEMENTATION_FAILED
- VERIFICATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `A4` in output JSON
- [ ] Output written to `generated_projects/{run_id}/A4/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill A4 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill A4 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill A4
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`A4`

### Capability Level
`A`

### Time Budget
90 minutes

### Depends On
- B1
- B3

### Objective
Analyze repo for modernization opportunities, prioritize, implement highest-value lowest-risk first step.

### Inputs
- repository_path
- inventory_report.json (B1)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/A4/modernization_report.json`

```json
{
  "findings": [
    {
      "description": "Outdated pytest pin",
      "evidence": [
        "requirements-dev.txt"
      ],
      "id": "F1",
      "priority": 1
    }
  ],
  "first_step": {
    "action": "Upgrade pytest to 8.x",
    "evidence": [
      "requirements-dev.txt:3"
    ],
    "files_changed": [
      "requirements-dev.txt"
    ]
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "A",
  "prioritized_plan": [
    {
      "action": "Upgrade pytest",
      "priority": 1
    }
  ],
  "rollback_notes": [
    "git revert HEAD"
  ],
  "scan_complete": true,
  "task_id": "A4",
  "verification": {
    "command": "pytest -q",
    "exit_code": 0
  },
  "warnings": []
}
```

### Eval Deliverables
- Findings with evidence
- Prioritized plan
- First step implemented
- Verification
- Rollback

### Validation
- first_step.files_changed non-empty
- verification.exit_code == 0
- DC-A4-01 through DC-A4-02 pass

### Failure Conditions
- NO_FINDINGS
- IMPLEMENTATION_FAILED
- VERIFICATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/advanced/A4_modernization_executable.skill.md`
- Eval blueprint: `eval_blueprints/A/A4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A4_modernization_executable_agent.md`

