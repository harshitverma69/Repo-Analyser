---
name: repo-analyser-b5-nodejs-greenfield
description: |
  Repo-Analyser B5 (BASIC) — Build equivalent transaction/balance service as Node.js API or CLI with tests and README.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Nodejs Greenfield (B5)

You are the **Nodejs Greenfield** in the Repo-Analyser deterministic eval framework.

**Objective:** Build equivalent transaction/balance service as Node.js API or CLI with tests and README.

**Capability level:** `B` · **Time budget:** 60 minutes · **Depends on:** `B4`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/B5/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `project_name` | Yes | New project directory name |
| `output_dir` | Yes | Absolute path for greenfield output |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Scaffold Node service
Create transaction/balance API or CLI under `output_dir/{project_name}/` with `package.json`, entry file, README.

Parity with B4 domain: POST/GET transactions, GET balance (or CLI equivalents).

## Phase 2 — Tests & proof
Add tests (jest/vitest/node:test). Run test command; record exit code.

Provide `run_proof` with sample request/response or CLI output.

## Phase 3 — Write JSON manifest
Write `generated_projects/{run_id}/B5/output.json` with `files_created`, `tests`, `readme_commands`, `run_proof`.

---

## Eval deliverables

- Node API or CLI
- Equivalent endpoints/commands
- Tests
- README

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/B5/greenfield_manifest.json`.

---

## Validation

- tests.count >= 3
- run_proof.exit_code == 0
- DC-B5-01 through DC-B5-02 pass

---

## Failure conditions

- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `B5` in output JSON
- [ ] Output written to `generated_projects/{run_id}/B5/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill B5 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill B5 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill B5
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`B5`

### Capability Level
`B`

### Time Budget
60 minutes

### Depends On
- B4

### Objective
Build equivalent transaction/balance service as Node.js API or CLI with tests and README.

### Inputs
- project_name (string)
- output_dir (absolute path)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/B5/greenfield_manifest.json`

```json
{
  "endpoints_or_commands": [
    "POST /transactions",
    "GET /balance"
  ],
  "files_created": [
    "src/index.js",
    "package.json",
    "tests/api.test.js"
  ],
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "B",
  "mode": "api",
  "project_path": "generated_projects/example-run/B5/tx-node",
  "readme_commands": {
    "install": [
      "npm install"
    ],
    "run": [
      "npm start"
    ],
    "test": [
      "npm test"
    ]
  },
  "run_proof": {
    "command": "npm test",
    "exit_code": 0
  },
  "scan_complete": true,
  "task_id": "B5",
  "tests": {
    "command": "npm test",
    "count": 3,
    "exit_code": 0
  },
  "warnings": []
}
```

### Eval Deliverables
- Node API or CLI
- Equivalent endpoints/commands
- Tests
- README

### Validation
- tests.count >= 3
- run_proof.exit_code == 0
- DC-B5-01 through DC-B5-02 pass

### Failure Conditions
- INPUT_CONTRACT_VIOLATION
- BUILD_FAILED
- TEST_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/basics/B5_nodejs_greenfield.skill.md`
- Eval blueprint: `eval_blueprints/B/B5_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/basics/B5_nodejs_greenfield_agent.md`

