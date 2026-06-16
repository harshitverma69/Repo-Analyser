## Skill: Ci Pipeline

### Task ID
`D3`

### Level
`INFRA`

### Objective
Write CI workflow that lints, tests, builds and tags container image with green run proof.

### Depends On
- B3
- I5

### Input Contract
```json
{
  "repository_path": "required",
  "ci_platform": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/infra_devops/D3_ci_pipeline_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill D3 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "cache_config": {
    "pip": "~/.cache/pip"
  },
  "failure_demo": {
    "broken_commit": "bad1234",
    "expected_fail_stage": "test"
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "pass_proof": {
    "command_or_link": "act push",
    "exit_code": 0
  },
  "scan_complete": true,
  "task_id": "D3",
  "warnings": [],
  "workflow_file": ".github/workflows/ci.yml"
}
```

### Validation Rules
- pass_proof.exit_code == 0
- failure_demo documents expected fail
- DC-D3-01 through DC-D3-02 pass

### Failure Conditions
- WORKFLOW_INVALID
- PIPELINE_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/infra/D3_ci_pipeline.skill.md`
- Eval blueprint: `eval_blueprints/D/D3_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D3_ci_pipeline_agent.md`

### Sources
- Agent: `agents/infra_devops/D3_ci_pipeline_agent.md`
- Blueprint: `eval_blueprints/D/D3_blueprint.md`
- Skill: `skills/infra/D3_ci_pipeline.skill.md`
