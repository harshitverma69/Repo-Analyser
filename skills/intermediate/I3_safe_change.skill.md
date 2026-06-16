## Skill: Safe Change

### Task ID
`I3`

### Level
`INTERMEDIATE`

### Objective
Make a small focused change in an unfamiliar module with minimal diff, test update, and verification log.

### Depends On
- B3

### Input Contract
```json
{
  "repository_path": "required",
  "change_spec": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/intermediate/I3_safe_change_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill I3 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "branch_or_diff_ref": "fix/validate-amount",
  "files_changed": [
    "app/services/transaction.py"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "I",
  "rationale": [
    "Add validation for negative amounts"
  ],
  "risk_assessment": {
    "factors": [
      "single file change"
    ],
    "level": "low"
  },
  "scan_complete": true,
  "task_id": "I3",
  "test_command": "pytest tests/test_transactions.py -q",
  "test_result": {
    "exit_code": 0
  },
  "verification_log": {
    "agent_suggested": [
      "Add guard clause"
    ],
    "manually_verified": [
      "Guard clause at line 42"
    ],
    "uncertain": []
  },
  "warnings": []
}
```

### Validation Rules
- files_changed non-empty
- test_result.exit_code == 0
- verification_log populated
- DC-I3-01 through DC-I3-03 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/intermediate/I3_safe_change.skill.md`
- Eval blueprint: `eval_blueprints/I/I3_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I3_safe_change_agent.md`

### Sources
- Agent: `agents/intermediate/I3_safe_change_agent.md`
- Blueprint: `eval_blueprints/I/I3_blueprint.md`
- Skill: `skills/intermediate/I3_safe_change.skill.md`
