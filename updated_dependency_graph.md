# Updated Dependency Graph

## Runtime package imports

```mermaid
flowchart TD
  subgraph public [Public API]
    SO[skill_orchestrator.py]
    SR[skill_runner.py]
  end

  subgraph orchestrator [runtime/orchestrator]
    PL[planner.py]
    DR[dependency_resolver.py]
    EX[executor.py]
    RA[result_aggregator.py]
    CLI[cli.py]
  end

  subgraph plugins [runtime/plugins]
    PB[base.py]
    PLG[loader.py]
    PR[registry.py]
  end

  subgraph core [Shared]
    MD[models.py]
    SP[skill_parser.py]
    DT[deterministic.py]
  end

  SO --> PL
  SO --> DR
  SR --> EX
  SR --> RA
  SR --> PL
  PL --> DR
  PL --> SP
  EX --> RA
  EX --> MD
  EX --> PL
  PLG --> EX
  PLG --> PR
  PLG --> MD
  RA --> MD
  RA --> PL
```

## Skill DAG (unchanged)

24 PML/OCL skills; wave 0 has no deps; B2/I1 depend on B1; etc.
Validate with:

```bash
make validate-dag
```

## Tools expand package

```
expand_agent_specs.py → expand/cli.py → expand/compiler.py
                                      → expand/parser.py
                                      → expand/phases_data.py
                                      → expand/template_engine.py
```

No circular imports between runtime subpackages.
