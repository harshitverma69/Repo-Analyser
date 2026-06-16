## Skill: Repo Artifact Inventory

### Task ID
`B1`

### Level
`BASIC`

### Objective
Inspect an unfamiliar repository and produce a deterministic inventory of classes, interfaces, services, controllers, models, repositories, jobs, consumers, configs, and utilities.

### Depends On
None

### Input Contract
```json
{
  "repository_path": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/basics/B1_repo_artifact_inventory_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill B1 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "artifacts": {
    "classes": [],
    "configurations": [],
    "consumers": [],
    "controllers": [
      {
        "file_path": "app/controllers/order.py",
        "name": "OrderController"
      }
    ],
    "interfaces": [],
    "jobs": [],
    "models": [],
    "repositories": [],
    "services": [
      {
        "file_path": "app/services/order.py",
        "name": "OrderService"
      }
    ],
    "utilities": []
  },
  "dependency_graph_summary": {
    "edges": [],
    "nodes": [
      "app"
    ]
  },
  "files_scanned": 142,
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "B",
  "limitations": [],
  "modules": [
    {
      "name": "app",
      "path": "app/"
    }
  ],
  "scan_complete": true,
  "task_id": "B1",
  "warnings": []
}
```

### Validation Rules
- files_scanned >= 1 for non-empty repositories
- Every artifact has non-empty file_path
- Major modules discovered with evidence paths
- DC-B1-01 through DC-B1-04 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION: repository_path missing or not a directory
- ZERO_ARTIFACTS: source files exist but zero artifacts extracted
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/basics/B1_repo_artifact_inventory.skill.md`
- Eval blueprint: `eval_blueprints/B/B1_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B1_repo_artifact_inventory_agent.md`

### Sources
- Agent: `agents/basics/B1_repo_artifact_inventory_agent.md`
- Blueprint: `eval_blueprints/B/B1_blueprint.md`
- Skill: `skills/basics/B1_repo_artifact_inventory.skill.md`
