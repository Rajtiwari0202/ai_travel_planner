# Research

Research question: does a coordinated multi-agent pipeline with deterministic multi-objective planning produce more feasible and preference-aligned itineraries than simpler deterministic baselines?

The included benchmark cases are synthetic and transparent. They are not a user study and must not be interpreted as user satisfaction results.

## Current Benchmark Scope

- 12 transparent synthetic cases
- 10 Indian destinations
- Cheapest-first, weighted ranker, CP-SAT optimizer, CP-SAT without weather, and CP-SAT without geospatial clustering
- Metrics include feasibility, budget violations, preference coverage, travel distance, weather conflicts, validation errors, latency, budget utilization, and alternative availability

## Run Experiments

```powershell
cd F:\travelAgenticAi
.\venv\Scripts\python.exe research\experiments\run_all.py
```

Or run individual stages:

```powershell
.\venv\Scripts\python.exe research\experiments\run_benchmarks.py
.\venv\Scripts\python.exe research\experiments\run_ablations.py
```

Outputs:

- `research/results/benchmark_results.csv`
- `research/results/ablation_summary.csv`
- `research/figures/benchmark_scores.png`
