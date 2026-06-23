# Slide Content

## 1. Title
Text: TravelAgenticAI, a local-first explainable multi-agent travel planner.
Diagram: system context.
Notes: State that it is a research demo, not a booking platform.
Duration: 20 seconds.

## 2. Problem
Text: Travel planning mixes preferences, budget, weather, distance, and feasibility.
Diagram: data flow.
Notes: Manual planning is fragmented and hard to verify.
Duration: 25 seconds.

## 3. Existing Limitations
Text: One-shot prompts can hallucinate prices and ignore constraints.
Diagram: trust boundary.
Notes: Explain estimated data honesty.
Duration: 25 seconds.

## 4. Proposed Solution
Text: Coordinated agents plus deterministic optimization.
Diagram: agent orchestration.
Notes: Agents produce structured facts; optimizer schedules.
Duration: 30 seconds.

## 5. Multi-Agent Architecture
Text: Intent, destination, transport, accommodation, weather, geospatial, optimizer, writer, critic.
Diagram: backend component.
Notes: Each stage has a clear role and event trail.
Duration: 35 seconds.

## 6. Optimization Approach
Text: OR-Tools CP-SAT optimizes budget-feasible schedules.
Diagram: optimization pipeline.
Notes: Mention heuristic fallback.
Duration: 35 seconds.

## 7. Product Workflow
Text: Form, progress, itinerary, budget, map, revision, export.
Diagram: frontend component.
Notes: Show live demo.
Duration: 40 seconds.

## 8. Technology Stack
Text: FastAPI, React, TypeScript, SQLAlchemy, OR-Tools, Docker, Render, Neon.
Diagram: container architecture.
Notes: Zero-cost defaults.
Duration: 25 seconds.

## 9. Research Methodology
Text: Synthetic benchmark, baselines, ablations.
Diagram: research pipeline.
Notes: Draft research, no fabricated user study.
Duration: 35 seconds.

## 10. Experimental Results
Text: CP-SAT compared with deterministic baselines.
Diagram: benchmark figure.
Notes: Point to reproducible CSVs.
Duration: 30 seconds.

## 11. Live Demo Flow
Text: Goa request, stream, revise, export.
Diagram: sequence diagram.
Notes: Use the exact demo input.
Duration: 50 seconds.

## 12. Limitations and Future Work
Text: Citations, user study, real inventory, auth, payments, stronger routing.
Diagram: deployment architecture.
Notes: Keep claims honest.
Duration: 30 seconds.
