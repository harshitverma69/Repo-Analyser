---
name: repo-analyser-i5-dockerize
description: |
  Repo-Analyser I5 (INTERMEDIATE) — Containerize a service so it builds and runs cleanly in Docker with health check proof.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Dockerize (I5)

You are the **Dockerize** in the Repo-Analyser deterministic eval framework.

**Objective:** Containerize a service so it builds and runs cleanly in Docker with health check proof.

**Capability level:** `I` · **Time budget:** 60 minutes · **Depends on:** None

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/I5/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `service_path` | Yes | Service root to containerize |
| `service_port` | Yes | Exposed port integer |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — Dockerfile & context
Write multi-stage or slim Dockerfile for `service_path`. Expose `service_port`.

Add `.dockerignore` if missing.

## Phase 2 — Build & run
`docker build` and `docker run` with health check endpoint.

Record `build_proof` and `health_check` with commands and exit codes.

## Phase 3 — Write JSON manifest
Write `generated_projects/{run_id}/I5/output.json`.

---

## Eval deliverables

- Dockerfile
- Build proof
- Container run proof
- Health/curl proof
- README

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/I5/docker_manifest.json`.

---

## Validation

- build_proof.exit_code == 0
- health_check.response_status == 200
- DC-I5-01 through DC-I5-02 pass

---

## Failure conditions

- BUILD_FAILED
- RUN_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `I5` in output JSON
- [ ] Output written to `generated_projects/{run_id}/I5/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill I5 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill I5 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill I5
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`I5`

### Capability Level
`I`

### Time Budget
60 minutes

### Depends On
- None

### Objective
Containerize a service so it builds and runs cleanly in Docker with health check proof.

### Inputs
- service_path (absolute path)
- service_port (integer)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/I5/docker_manifest.json`

```json
{
  "build_proof": {
    "command": "docker build -t tx-service .",
    "exit_code": 0
  },
  "dockerfile_path": "Dockerfile",
  "generated_at": "2026-06-16T12:00:00Z",
  "health_check": {
    "command": "curl -sf http://localhost:8080/health",
    "response_body_sample": {
      "status": "ok"
    },
    "response_status": 200
  },
  "level": "I",
  "readme_commands": {
    "build": [
      "docker build -t tx-service ."
    ],
    "curl_proof": [
      "curl http://localhost:8080/health"
    ],
    "run": [
      "docker run -p 8080:8080 tx-service"
    ]
  },
  "run_proof": {
    "command": "docker run -d -p 8080:8080 tx-service",
    "exit_code": 0
  },
  "scan_complete": true,
  "task_id": "I5",
  "warnings": []
}
```

### Eval Deliverables
- Dockerfile
- Build proof
- Container run proof
- Health/curl proof
- README

### Validation
- build_proof.exit_code == 0
- health_check.response_status == 200
- DC-I5-01 through DC-I5-02 pass

### Failure Conditions
- BUILD_FAILED
- RUN_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/intermediate/I5_dockerize.skill.md`
- Eval blueprint: `eval_blueprints/I/I5_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/intermediate/I5_dockerize_agent.md`

