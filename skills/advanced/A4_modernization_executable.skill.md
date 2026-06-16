## Skill: Modernization Executable

### Task ID
`A4`

### Level
`ADVANCED`

### Objective
Analyze repo for modernization opportunities, prioritize, implement highest-value lowest-risk first step.

### Depends On
- B1
- B3

### Input Contract
```json
{
  "repository_path": "required",
  "inventory_report.json": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/advanced/A4_modernization_executable_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill A4 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
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

### Validation Rules
- first_step.files_changed non-empty
- verification.exit_code == 0
- DC-A4-01 through DC-A4-02 pass

### Failure Conditions
- NO_FINDINGS
- IMPLEMENTATION_FAILED
- VERIFICATION_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/advanced/A4_modernization_executable.skill.md`
- Eval blueprint: `eval_blueprints/A/A4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A4_modernization_executable_agent.md`

### Sources
- Agent: `agents/advanced/A4_modernization_executable_agent.md`
- Blueprint: `eval_blueprints/A/A4_blueprint.md`
- Skill: `skills/advanced/A4_modernization_executable.skill.md`
