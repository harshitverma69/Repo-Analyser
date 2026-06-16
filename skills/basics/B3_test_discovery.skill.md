## Skill: Test Discovery

### Task ID
`B3`

### Level
`BASIC`

### Objective
Find test framework, config file, relevant test files, and exact commands to run tests for a module.

### Depends On
None

### Input Contract
```json
{
  "repository_path": "required",
  "module_path": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/basics/B3_test_discovery_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill B3 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "command_result": {
    "exit_code": 0,
    "stderr_hash": "",
    "stdout_hash": "abc123"
  },
  "commands": {
    "coverage": "pytest --cov=app -q",
    "integration": "pytest tests/integration -q",
    "unit": "pytest -q"
  },
  "config_files": [
    "pytest.ini"
  ],
  "failures": [],
  "framework": "pytest",
  "generated_at": "2026-06-16T12:00:00Z",
  "interpretation": [],
  "level": "B",
  "scan_complete": true,
  "task_id": "B3",
  "test_files": [
    "tests/test_transactions.py"
  ],
  "warnings": []
}
```

### Validation Rules
- framework is non-empty for repos with tests
- At least one test command defined
- test_files paths exist on disk
- DC-B3-01 through DC-B3-03 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- ZERO_ARTIFACTS: no test framework detected
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/basics/B3_test_discovery.skill.md`
- Eval blueprint: `eval_blueprints/B/B3_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B3_test_discovery_agent.md`

### Sources
- Agent: `agents/basics/B3_test_discovery_agent.md`
- Blueprint: `eval_blueprints/B/B3_blueprint.md`
- Skill: `skills/basics/B3_test_discovery.skill.md`
