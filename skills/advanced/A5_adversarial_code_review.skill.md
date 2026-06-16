## Skill: Adversarial Code Review

### Task ID
`A5`

### Level
`ADVANCED`

### Objective
Review agent-generated PR for correctness, security, test, performance, maintainability issues; propose fixes.

### Depends On
None

### Input Contract
```json
{
  "diff_or_pr_ref": "required",
  "repository_path": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/advanced/A5_adversarial_code_review_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON + output.md via `python3 -m runtime.skill_finish write --run-id {run_id} --skill A5 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "generated_at": "2026-06-16T12:00:00Z",
  "issues": [
    {
      "category": "security",
      "description": "Missing input validation on amount",
      "file_path": "app/main.py",
      "id": "ISS-1",
      "line": 10,
      "severity": "blocking",
      "suggested_fix": "Add Pydantic constraints",
      "verification_steps": [
        "pytest tests/test_validation.py"
      ]
    }
  ],
  "level": "A",
  "scan_complete": true,
  "task_id": "A5",
  "warnings": []
}
```

### Validation Rules
- Every issue has category and severity
- blocking issues have suggested_fix
- DC-A5-01 through DC-A5-02 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION: no diff
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/advanced/A5_adversarial_code_review.skill.md`
- Eval blueprint: `eval_blueprints/A/A5_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A5_adversarial_code_review_agent.md`

### Sources
- Agent: `agents/advanced/A5_adversarial_code_review_agent.md`
- Blueprint: `eval_blueprints/A/A5_blueprint.md`
- Skill: `skills/advanced/A5_adversarial_code_review.skill.md`
