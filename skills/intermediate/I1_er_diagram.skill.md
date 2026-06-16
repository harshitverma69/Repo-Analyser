## Skill: Er Diagram

### Task ID
`I1`

### Level
`INTERMEDIATE`

### Objective
Build ER diagram for all tables and entities from repo source only; cite source file for every claim.

### Depends On
- B1

### Input Contract
```json
{
  "repository_path": "required",
  "inventory_report.json": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/intermediate/I1_er_diagram_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill I1 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "I",
  "mermaid_er": "erDiagram\n  transactions {\n    uuid id PK\n  }",
  "relationships": [],
  "scan_complete": true,
  "tables": [
    {
      "columns": [
        {
          "name": "id",
          "type": "uuid"
        }
      ],
      "entity": "Transaction",
      "name": "transactions",
      "primary_keys": [
        "id"
      ],
      "source_file": "app/models/transaction.py"
    }
  ],
  "task_id": "I1",
  "warnings": []
}
```

### Validation Rules
- Every table has source_file
- mermaid_er parses
- DC-I1-01 through DC-I1-03 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/intermediate/I1_er_diagram.skill.md`
- Eval blueprint: `eval_blueprints/I/I1_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I1_er_diagram_agent.md`

### Sources
- Agent: `agents/intermediate/I1_er_diagram_agent.md`
- Blueprint: `eval_blueprints/I/I1_blueprint.md`
- Skill: `skills/intermediate/I1_er_diagram.skill.md`
