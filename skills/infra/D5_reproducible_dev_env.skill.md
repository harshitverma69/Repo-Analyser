## Skill: Reproducible Dev Env

### Task ID
`D5`

### Level
`INFRA`

### Objective
Bootstrap repo from fresh clone with single command; tests pass on clean machine.

### Depends On
- B3

### Input Contract
```json
{
  "repository_path": "required",
  "bootstrap_type": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/infra_devops/D5_reproducible_dev_env_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill D5 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "bootstrap_command": "make bootstrap",
  "bootstrap_proof": {
    "command": "make bootstrap",
    "exit_code": 0,
    "output_hash": "def456"
  },
  "config_files": [
    ".devcontainer/devcontainer.json"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "previously_implicit": [
    "python 3.11",
    "libpq-dev",
    "DATABASE_URL env var"
  ],
  "scan_complete": true,
  "task_id": "D5",
  "test_proof": {
    "command": "pytest -q",
    "exit_code": 0
  },
  "warnings": []
}
```

### Validation Rules
- bootstrap_proof.exit_code == 0
- test_proof.exit_code == 0
- DC-D5-01 through DC-D5-02 pass

### Failure Conditions
- BOOTSTRAP_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/infra/D5_reproducible_dev_env.skill.md`
- Eval blueprint: `eval_blueprints/D/D5_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D5_reproducible_dev_env_agent.md`

### Sources
- Agent: `agents/infra_devops/D5_reproducible_dev_env_agent.md`
- Blueprint: `eval_blueprints/D/D5_blueprint.md`
- Skill: `skills/infra/D5_reproducible_dev_env.skill.md`
