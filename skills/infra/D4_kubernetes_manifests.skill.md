## Skill: Kubernetes Manifests

### Task ID
`D4`

### Level
`INFRA`

### Objective
Write K8s manifests, validate with dry-run/kubeval, deploy on kind/minikube with curl proof.

### Depends On
- I5

### Input Contract
```json
{
  "service_path": "required",
  "cluster": "required"
}
```

### Execution Steps (DETERMINISTIC ONLY)
- Read agent spec: `agents/infra_devops/D4_kubernetes_manifests_agent.md`
- Apply deterministic rules from `core/execution_rules.md`
- Write JSON + output.md via `python3 -m runtime.skill_finish write --run-id {run_id} --skill D4 --payload-file <payload.json>` (auto-opens CLI UI)
- Validate output against Output Contract

### Output Contract (STRICT JSON)
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

### Validation Rules
- dry_run_proof.exit_code == 0
- curl_proof.response_status == 200
- DC-D4-01 through DC-D4-02 pass

### Failure Conditions
- VALIDATION_FAILED
- APPLY_FAILED
- CURL_FAILED
- OUTPUT_SCHEMA_VIOLATION
- --
- Skill spec: `skills/infra/D4_kubernetes_manifests.skill.md`
- Eval blueprint: `eval_blueprints/D/D4_blueprint.md`
- Execution rules: `core/execution_rules.md`
- Agent spec path: `agents/infra_devops/D4_kubernetes_manifests_agent.md`

### Sources
- Agent: `agents/infra_devops/D4_kubernetes_manifests_agent.md`
- Blueprint: `eval_blueprints/D/D4_blueprint.md`
- Skill: `skills/infra/D4_kubernetes_manifests.skill.md`
