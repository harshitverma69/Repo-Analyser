## Skill: Parallel Worktrees Execute

### Task ID
`A2`

### Level
`ADVANCED`

### Objective
Create two parallel worktrees, make independent changes, reconcile cleanly with test proof.

### Depends On
- A1

### Input Contract
```json
{
  "repository_path": "required",
  "worktree_plan.json": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/advanced/A2_parallel_worktrees_execute_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON via `python3 -m runtime.skill_finish write --run-id {run_id} --skill A2 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
```json
{
  "commands": [
    "git worktree add ../repo-wt-api -b feature/api"
  ],
  "conflicts": [],
  "generated_at": "2026-06-16T12:00:00Z",
  "lane_outputs": {
    "lane-api": {
      "commit": "abc1234",
      "files": [
        "app/controllers/transaction.py"
      ]
    }
  },
  "level": "A",
  "merge_steps": [
    "git merge feature/api",
    "git merge feature/worker"
  ],
  "scan_complete": true,
  "task_id": "A2",
  "test_result": {
    "command": "pytest -q",
    "exit_code": 0
  },
  "warnings": [],
  "worktrees": [
    {
      "branch": "feature/api",
      "name": "wt-lane-api"
    },
    {
      "branch": "feature/worker",
      "name": "wt-lane-worker"
    }
  ]
}
```

### Validation Rules
- 2 worktrees created
- test_result.exit_code == 0
- DC-A2-01 through DC-A2-02 pass

### Failure Conditions
- WORKTREE_CREATE_FAILED
- MERGE_CONFLICT_UNRESOLVED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/advanced/A2_parallel_worktrees_execute.skill.md`
- Eval blueprint: `eval_blueprints/A/A2_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/advanced/A2_parallel_worktrees_execute_agent.md`

### Sources
- Agent: `agents/advanced/A2_parallel_worktrees_execute_agent.md`
- Blueprint: `eval_blueprints/A/A2_blueprint.md`
- Skill: `skills/advanced/A2_parallel_worktrees_execute.skill.md`
