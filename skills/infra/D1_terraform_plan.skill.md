## Skill: Terraform Plan

### Task ID
`D1`

### Level
`INFRA`

### Objective
Write Terraform for small service that passes validate and produces clean plan against test backend.

### Depends On
None

### Input Contract
```json
{
  "output_dir": "required",
  "provider": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/infra_devops/D1_terraform_plan_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill D1 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "plan_proof": {
    "changes_summary": {
      "add": 3,
      "change": 0,
      "destroy": 0
    },
    "command": "terraform plan",
    "exit_code": 0
  },
  "readme": {
    "apply": [
      "terraform apply -auto-approve"
    ],
    "destroy": [
      "terraform destroy -auto-approve"
    ]
  },
  "scan_complete": true,
  "task_id": "D1",
  "tf_files": [
    "main.tf",
    "variables.tf"
  ],
  "validate_proof": {
    "command": "terraform validate",
    "exit_code": 0
  },
  "variables": {
    "region": "us-east-1"
  },
  "warnings": []
}
```

### Validation Rules
- validate_proof.exit_code == 0
- plan_proof.exit_code == 0
- DC-D1-01 through DC-D1-02 pass

### Failure Conditions
- VALIDATE_FAILED
- PLAN_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/infra/D1_terraform_plan.skill.md`
- Eval blueprint: `eval_blueprints/D/D1_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D1_terraform_plan_agent.md`

### Sources
- Agent: `agents/infra_devops/D1_terraform_plan_agent.md`
- Blueprint: `eval_blueprints/D/D1_blueprint.md`
- Skill: `skills/infra/D1_terraform_plan.skill.md`
