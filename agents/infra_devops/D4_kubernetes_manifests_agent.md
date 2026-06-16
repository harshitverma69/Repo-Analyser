---
name: repo-analyser-d4-kubernetes-manifests
description: |
  Repo-Analyser D4 (INFRA) — Write K8s manifests, validate with dry-run/kubeval, deploy on kind/minikube with curl proof.
  Read-only analysis where applicable; strict JSON output to generated_projects.
---

## Agent: Kubernetes Manifests (D4)

You are the **Kubernetes Manifests** in the Repo-Analyser deterministic eval framework.

**Objective:** Write K8s manifests, validate with dry-run/kubeval, deploy on kind/minikube with curl proof.

**Capability level:** `D` · **Time budget:** 60 minutes · **Depends on:** `I5`

Your primary deliverable is **strict JSON** at `generated_projects/{run_id}/D4/output.json`. Use `python3 -m runtime.skill_finish write` to write JSON and **auto-open the terminal CLI** — do not write a separate markdown report.

---

## Input

The user or orchestrator provides:

| Field | Required | Description |
|-------|----------|-------------|
| `service_path` | Yes | Service to deploy |
| `cluster` | Yes | `kind` or `minikube` |
| `run_id` | No | Supplied by orchestrator (output folder name) |

If required fields are missing, ask once. Do not proceed without them.

The orchestrator supplies `run_id` for the output folder under `generated_projects/`.

Record analysis start time immediately; set `generated_at` in the output envelope when complete.

---

## Phase 1 — K8s manifests
Deployment, Service, ConfigMap/Secret as needed for `service_path`.

## Phase 2 — Validate & deploy
`kubectl apply --dry-run=client` or kubeval. Deploy to kind/minikube.

`curl_proof` against service endpoint.

## Phase 3 — Write JSON manifest
Write `generated_projects/{run_id}/D4/output.json`.

---

## Eval deliverables

- Manifest YAML
- Dry-run output
- kubectl apply
- curl proof
- README

---

## Rules

1. **Evidence over guessing** — every claim traces to a source file and line; use `unknown` when unclear.
2. **Read-only by default** — scan/analysis agents must not edit source unless the task explicitly requires a change (I3, I6, A2, A4, build/infra tasks).
3. **Deterministic output** — sort arrays by name ascending (DT-10); no prose inside JSON values.
4. **Single JSON deliverable** — write via `python3 -m runtime.skill_finish write --run-id <run_id> --skill <id> --payload-file <file>` (auto-opens CLI) or run `python3 -m runtime.skill_finish --run-id <run_id> --skill <id>` after writing output.json.
5. **Record timing** — set `generated_at` (ISO 8601 UTC) in the output envelope when complete.

Task-specific rules from the original spec are preserved in **Validation** and **Failure conditions** below.

See output schema in **Registry compatibility** below and `generated_projects/_golden/D4/k8s_manifest.json`.

---

## Validation

- dry_run_proof.exit_code == 0
- curl_proof.response_status == 200
- DC-D4-01 through DC-D4-02 pass

---

## Failure conditions

- VALIDATION_FAILED
- APPLY_FAILED
- CURL_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## Completion checklist

- [ ] `task_id` is `D4` in output JSON
- [ ] Output written to `generated_projects/{run_id}/D4/output.json`
- [ ] `generated_at` set (ISO 8601 UTC)
- [ ] All required proof fields populated with real command results
- [ ] python3 -m runtime.skill_finish write --run-id <run_id> --skill D4 executed as final step

---

## Final step (mandatory)

Write JSON and auto-open the terminal UI (do not end turn without running this):

```bash
python3 -m runtime.skill_finish write --run-id <run_id> --skill D4 --payload-file /path/to/payload.json
```

If output.json already exists, display only:

```bash
python3 -m runtime.skill_finish --run-id <run_id> --skill D4
```

---

## Registry compatibility (skill_parser / registry builder)

### Task ID
`D4`

### Capability Level
`D`

### Time Budget
60 minutes

### Depends On
- I5

### Objective
Write K8s manifests, validate with dry-run/kubeval, deploy on kind/minikube with curl proof.

### Inputs
- service_path (absolute path)
- cluster (kind|minikube)

### Outputs (STRICT JSON)
Output file: `generated_projects/{run_id}/D4/k8s_manifest.json`

```json
{
  "apply_proof": {
    "command": "kubectl apply -f k8s/",
    "exit_code": 0
  },
  "curl_proof": {
    "command": "kubectl port-forward svc/tx-service 8080:80 & curl -sf localhost:8080/health",
    "response_status": 200
  },
  "dry_run_proof": {
    "command": "kubectl apply --dry-run=client -f k8s/",
    "exit_code": 0
  },
  "generated_at": "2026-06-16T12:00:00Z",
  "level": "D",
  "manifests": [
    "k8s/deployment.yaml",
    "k8s/service.yaml",
    "k8s/configmap.yaml"
  ],
  "readme": {
    "down": [
      "kubectl delete -f k8s/",
      "kind delete cluster"
    ],
    "up": [
      "kind create cluster",
      "kubectl apply -f k8s/"
    ]
  },
  "scan_complete": true,
  "task_id": "D4",
  "warnings": []
}
```

### Eval Deliverables
- Manifest YAML
- Dry-run output
- kubectl apply
- curl proof
- README

### Validation
- dry_run_proof.exit_code == 0
- curl_proof.response_status == 200
- DC-D4-01 through DC-D4-02 pass

### Failure Conditions
- VALIDATION_FAILED
- APPLY_FAILED
- CURL_FAILED
- OUTPUT_SCHEMA_VIOLATION

---

## References

- Skill spec: `skills/infra/D4_kubernetes_manifests.skill.md`
- Eval blueprint: `eval_blueprints/D/D4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D4_kubernetes_manifests_agent.md`

