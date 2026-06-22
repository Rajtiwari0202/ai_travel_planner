from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    source = ROOT / "research" / "results" / "benchmark_results.csv"
    target = ROOT / "research" / "results" / "ablation_summary.csv"
    rows = list(csv.DictReader(source.open(encoding="utf-8")))
    systems = sorted({row["system"] for row in rows})
    summary = []
    for system in systems:
        subset = [row for row in rows if row["system"] == system]
        summary.append(
            {
                "system": system,
                "mean_feasible": round(sum(float(row["itinerary_feasible"]) for row in subset) / len(subset), 4),
                "mean_budget_violation": round(sum(float(row["budget_violation"]) for row in subset) / len(subset), 4),
                "mean_score": round(sum(float(row["total_score"]) for row in subset) / len(subset), 4),
                "mean_weather_conflicts": round(
                    sum(float(row["weather_conflict_count"]) for row in subset) / len(subset),
                    4,
                ),
                "mean_total_travel_distance_km": round(
                    sum(float(row["total_travel_distance_km"]) for row in subset) / len(subset),
                    4,
                ),
                "mean_cost_utilization": round(
                    sum(float(row["estimated_cost_utilization"]) for row in subset) / len(subset),
                    4,
                ),
                "mean_planning_latency_ms": round(
                    sum(float(row["planning_latency_ms"]) for row in subset) / len(subset),
                    4,
                ),
                "alternative_availability_rate": round(
                    sum(float(row["alternative_plan_available"]) for row in subset) / len(subset),
                    4,
                ),
            }
        )
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
