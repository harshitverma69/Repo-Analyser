---
name: cac-os-i6-bug-diagnosis
description: |
  CAC-OS I6 (INTERMEDIATE) — Reproduce seeded bug, identify root cause with file paths, apply minimal fix, verify with command proof.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Bug Diagnosis (I6)

You are the **Bug Diagnosis** in the CAC-OS deterministic eval framework.

**Objective:** Reproduce seeded bug, identify root cause with file paths, apply minimal fix, verify with command proof.

**Capability level:** `I` · **Time budget:** 60 minutes · **Depends on:** `I2`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/I6/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `repository_path` | Yes | Repository root |
| `bug_context` | Yes | `{symptoms, reproduction_hint}` |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Reproduce bug
Use `bug_context` symptoms and hints. Run reproduction steps; capture logs/errors.

## Phase 2 — Root cause analysis
Trace with I2-style static analysis if needed. Identify file paths and lines for root cause.

## Phase 3 — Minimal fix & verify
Apply smallest correct fix. Run verification commands; populate `verification` log.

## Phase 4 — Write JSON output
Write `generated_projects/{run_id}/I6/output.json` with root cause, fix, and proof.

---

## Eval deliverables

- Reproduction
- Root cause paths
- Minimal fix
- Verification result
- Agent vs verified

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/I6/bug_fix_report.json`.

---

## Validation

- root_cause.file_path exists
- verification.exit_code == 0
- DC-I6-01 through DC-I6-03 pass

---

## Failure conditions

- REPRODUCTION_FAILED
- FIX_FAILED
- VERIFICATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `I6` in output JSON
- [ ] Output written to `generated_projects/{run_id}/I6/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill I6 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill I6 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill I6
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`I6`

### Capability Level
`I`

### Time Budget
60 minutes

### Depends On
- I2

### Objective
Reproduce seeded bug, identify root cause with file paths, apply minimal fix, verify with command proof.

### Inputs
- repository_path
- bug_context {symptoms, reproduction_hint}

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/I6/bug_fix_report.json`

```json
{
  "fix": {
    "diff_summary": "Add null check before persist",
    "files_changed": [
      "app/services/transaction.py"
    ]
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "I",
  "reproduction_steps": [
    "pytest tests/test_bug.py -q"
  ],
  "root_cause": {
    "description": "Null amount not checked",
    "file_path": "app/services/transaction.py",
    "line": 55
  },
  "scan_complete": true,
  "task_id": "I6",
  "verification": {
    "command": "pytest tests/test_bug.py -q",
    "exit_code": 0
  },
  "verification_log": {
    "agent_suggested": [
      "Null check"
    ],
    "manually_verified": [
      "Confirmed NPE resolved"
    ]
  },
  "warnings": []
}
```

### Eval Deliverables
- Reproduction
- Root cause paths
- Minimal fix
- Verification result
- Agent vs verified

### Validation
- root_cause.file_path exists
- verification.exit_code == 0
- DC-I6-01 through DC-I6-03 pass

### Failure Conditions
- REPRODUCTION_FAILED
- FIX_FAILED
- VERIFICATION_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/intermediate/I6_bug_diagnosis.skill.md`
- Eval blueprint: `eval_blueprints/I/I6_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I6_bug_diagnosis_agent.md`

