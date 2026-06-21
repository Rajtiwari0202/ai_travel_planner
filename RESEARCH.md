# Research

Research question: does a coordinated multi-agent pipeline with deterministic multi-objective planning produce more feasible and preference-aligned itineraries than simpler deterministic baselines?

The included benchmark cases are synthetic and transparent. They are not a user study and must not be interpreted as user satisfaction results.

## Run Experiments

```powershell
cd F:\travelAgenticAi
.\venv\Scripts\python.exe research\experiments\run_benchmarks.py
.\venv\Scripts\python.exe research\experiments\run_ablations.py
```

Outputs:

- `research/results/benchmark_results.csv`
- `research/results/ablation_summary.csv`
- `research/figures/benchmark_scores.png`
