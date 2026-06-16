## Skill: Bug Diagnosis

### Task ID
`I6`

### Level
`INTERMEDIATE`

### Objective
Reproduce seeded bug, identify root cause with file paths, apply minimal fix, verify with command proof.

### Depends On
- I2

### Input Contract
```json
{
  "repository_path": "required",
  "bug_context": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/intermediate/I6_bug_diagnosis_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill I6 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
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

### Validation Rules
- root_cause.file_path exists
- verification.exit_code == 0
- DC-I6-01 through DC-I6-03 pass

### Failure Conditions
- REPRODUCTION_FAILED
- FIX_FAILED
- VERIFICATION_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/intermediate/I6_bug_diagnosis.skill.md`
- Eval blueprint: `eval_blueprints/I/I6_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I6_bug_diagnosis_agent.md`

### Sources
- Agent: `agents/intermediate/I6_bug_diagnosis_agent.md`
- Blueprint: `eval_blueprints/I/I6_blueprint.md`
- Skill: `skills/intermediate/I6_bug_diagnosis.skill.md`
