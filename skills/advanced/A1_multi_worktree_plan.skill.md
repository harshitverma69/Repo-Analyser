## Skill: Multi Worktree Plan

### Task ID
`A1`

### Level
`ADVANCED`

### Objective
Split one feature/analysis task into parallel worktrees or agent sessions without merge chaos.

### Depends On
None

### Input Contract
```json
{
  "repository_path": "required",
  "task_description": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/advanced/A1_multi_worktree_plan_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON + output.md via `python3 -m runtime.skill_finish write --run-id {run_id} --skill A1 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "agent_prompts": {
    "lane-api": "Implement POST /transactions only",
    "lane-worker": "Implement queue consumer only"
  },
  "conflict_plan": [
    "models/ may conflict \u2014 merge lane-api first"
  ],
  "decomposition": [
    {
      "lane_id": "lane-api",
      "scope": "API endpoints"
    },
    {
      "lane_id": "lane-worker",
      "scope": "Background worker"
    }
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "A",
  "merge_order": [
    "lane-api",
    "lane-worker"
  ],
  "scan_complete": true,
  "shared_constraints": [
    "Do not modify shared models without merge review"
  ],
  "task_id": "A1",
  "verification_plan": [
    "pytest -q after merge"
  ],
  "warnings": [],
  "worktrees": [
    {
      "lane_id": "lane-api",
      "name": "wt-lane-api-feature",
      "path": "../repo-wt-api"
    }
  ]
}
```

### Validation Rules
- lanes have disjoint scopes
- merge_order defined
- DC-A1-01 through DC-A1-02 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- OVERLAPPING_LANE_SCOPE
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/advanced/A1_multi_worktree_plan.skill.md`
- Eval blueprint: `eval_blueprints/A/A1_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A1_multi_worktree_plan_agent.md`

### Sources
- Agent: `agents/advanced/A1_multi_worktree_plan_agent.md`
- Blueprint: `eval_blueprints/A/A1_blueprint.md`
- Skill: `skills/advanced/A1_multi_worktree_plan.skill.md`
