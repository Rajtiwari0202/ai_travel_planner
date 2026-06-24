# MASTER CODEX PROMPT — PRODUCTION-GRADE AGENTIC AI TRAVEL PLANNER

You are the principal software architect, senior full-stack engineer, AI systems engineer, optimization researcher, UI/UX engineer, QA engineer, DevOps engineer, security reviewer, and technical writer responsible for transforming this repository into a production-quality, research-paper-grade Agentic AI Travel Planner.

Do not produce another toy hackathon prototype. Build a coherent, tested, explainable system that can be demonstrated locally without requiring any paid service.

## 1. Repository context

The repository already contains an early working implementation:

* React + TypeScript + Vite frontend
* Tailwind CSS
* FastAPI backend
* ResearchAgent and OptimizerAgent prototypes
* CSV-based flight, hotel, and activity data
* OpenAI-compatible narrative generation with a fallback
* Weather integration attempt
* React Leaflet map integration attempt
* Budget breakdown
* Animated agent loading UI
* GitHub README and MIT license

The existing implementation has architectural and correctness problems, including:

* loosely typed frontend data using `any`
* repeated or inconsistent backend models
* hardcoded trip duration
* browser-side geocoding
* itinerary output missing structured destination coordinates and dates
* weather and map data not reliably connected to itinerary days
* simplistic scoring
* inaccurate room and traveler cost assumptions
* fake-looking agent progress rather than real streamed progress
* weak error handling
* no persistence layer
* no comprehensive tests
* no reproducible research evaluation
* no production-oriented documentation

Inspect the repository before changing anything. Do not assume the exact file structure or dependency versions. Read all relevant files, run the current application, inspect Git status, and identify what already works.

Preserve working functionality while replacing weak implementations incrementally.

## 2. Primary mission

Build a complete Agentic AI Travel Planning and Multi-Objective Itinerary Optimization Platform that:

1. Interprets a traveler’s natural-language and structured requirements.
2. Researches candidate transport, accommodation, attractions, weather, geography, and destination information.
3. Scores and optimizes alternatives under budget, time, distance, interest, weather, diversity, and feasibility constraints.
4. Produces a structured, explainable, editable day-by-day itinerary.
5. Streams real agent progress to the frontend.
6. Supports follow-up changes such as:

   * “Reduce the budget to ₹25,000.”
   * “Add more adventure.”
   * “Avoid outdoor activities on rainy days.”
   * “Replace Day 2 with historical places.”
7. Shows maps, weather, budget allocation, score explanations, assumptions, and data-source labels.
8. Operates locally using free and open-source software.
9. Generates reproducible experiment results and a research-paper draft.
10. Passes frontend, backend, integration, and end-to-end tests.

## 3. Non-negotiable constraints

### Cost

The default application must require zero paid services.

Use only:

* open-source libraries
* free public datasets
* free APIs that do not require payment
* local inference where practical
* deterministic fallbacks where external services are unavailable

Do not require OpenAI, Anthropic, paid Google APIs, paid map APIs, paid databases, or paid hosting.

Optional paid-provider adapters may exist, but:

* they must be disabled by default
* they must not be required for tests
* they must not be required for the demo
* no secret may be committed
* the application must work without them

### Data honesty

Never describe synthetic, curated, cached, or estimated data as live data.

The UI must visibly distinguish:

* Estimated flight price
* Estimated accommodation price
* Public/open-data attraction
* Live weather forecast
* Cached result
* Synthetic demonstration data

Do not build booking or payment functionality. This is an itinerary decision-support system, not a booking engine.

### Security

* Never hardcode API keys.
* Never read or expose secret values in logs.
* Maintain `.env.example` using placeholders only.
* Ensure `.env`, virtual environments, build directories, databases, caches, and `node_modules` are ignored.
* Do not modify or expose Git credentials.
* Do not push to GitHub automatically.
* Do not change Git remotes.
* Do not delete user files without explicit justification.
* Validate and sanitize all inputs.
* Restrict CORS through environment configuration.
* Add safe request timeouts and error handling.
* Add basic rate limiting where appropriate.
* Avoid arbitrary code execution and unsafe deserialization.

### Engineering quality

* No unexplained `any` types.
* No duplicated schemas.
* No hardcoded three-day trip.
* No fake timers pretending to be agent progress.
* No silent error swallowing.
* No unbounded external API calls.
* No fabricated research results.
* No completion claim unless builds and tests pass.

## 4. Execution protocol

Work autonomously in phases.

Before implementation:

1. Inspect the complete repository.
2. Run:

   * Git status
   * frontend install/build/lint/tests where available
   * backend dependency installation and tests where available
3. Document existing failures.
4. Create:

   * `IMPLEMENTATION_PLAN.md`
   * `PROJECT_STATUS.md`
   * `AGENTS.md`
   * `docs/architecture/`
5. Write a phased plan with dependencies and acceptance criteria.
6. Then begin implementation without waiting for approval unless:

   * an operation is destructive
   * a required decision cannot be inferred
   * a credential is genuinely required
   * two incompatible architectural options have major consequences

After each phase:

* run relevant tests
* run relevant builds
* fix failures
* update `PROJECT_STATUS.md`
* list changed files
* record remaining risks
* make a small local Git commit only if the environment permits it
* never push

Continue until every mandatory acceptance criterion is either complete or explicitly documented as blocked.

## 5. Target architecture

Use a modular monorepo structure similar to:

```text
ai-trip-planner/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── planner/
│   │   │   ├── itinerary/
│   │   │   ├── agents/
│   │   │   ├── map/
│   │   │   ├── weather/
│   │   │   ├── budget/
│   │   │   └── assistant/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/
│   │   ├── types/
│   │   └── test/
│   ├── package.json
│   └── ...
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── agents/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── providers/
│   │   │   ├── optimization/
│   │   │   ├── geospatial/
│   │   │   ├── weather/
│   │   │   └── narrative/
│   │   ├── repositories/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   ├── data/
│   ├── migrations/
│   └── pyproject.toml
├── research/
│   ├── paper/
│   ├── experiments/
│   ├── datasets/
│   ├── results/
│   └── figures/
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── decisions/
│   ├── demo/
│   └── deployment/
├── docker-compose.yml
├── .github/workflows/
├── AGENTS.md
├── IMPLEMENTATION_PLAN.md
├── PROJECT_STATUS.md
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── .env.example
```

Adjust this structure if the existing repository makes another organization clearly better. Explain major architectural decisions in ADR files.

## 6. Technology choices

### Frontend

Retain and modernize:

* React
* TypeScript with strict mode
* Vite
* Tailwind CSS
* Framer Motion
* React Leaflet
* OpenStreetMap tiles

Add only where justified:

* React Router for pages
* TanStack Query for server state
* Zod for runtime API-response validation
* React Hook Form for validated forms
* Recharts for budget and score visualizations
* Vitest and React Testing Library
* Playwright for end-to-end tests

Do not replace the frontend framework.

### Backend

Use:

* Python 3.12-compatible code
* FastAPI
* Pydantic v2
* `httpx` for asynchronous HTTP requests
* SQLAlchemy 2 or SQLModel
* SQLite as the default database
* Alembic for migrations
* structured logging
* pytest and pytest-asyncio
* Ruff
* mypy or pyright-compatible typing

Prefer `httpx` over synchronous `requests` inside asynchronous application paths.

### Agent orchestration

Use an explicit typed orchestration graph.

LangGraph may be used because it is open source, but only if it improves state management and observability. Otherwise implement a clear typed state machine.

The orchestration layer must:

* maintain shared typed planning state
* record each agent’s input, output, duration, and status
* emit real events through Server-Sent Events
* support retries and timeouts
* support cancellation
* expose errors without leaking secrets
* support deterministic testing with mocked providers

### Local AI

Implement a provider interface such as:

```python
class LLMProvider(Protocol):
    async def generate_structured(...): ...
    async def generate_text(...): ...
```

Provide:

1. `OllamaLLMProvider`

   * default local AI option
   * configurable model through environment variables
   * document a lightweight quantized model suitable for a 16 GB Windows laptop
2. `TemplateLLMProvider`

   * deterministic zero-dependency fallback
   * ensures the complete system works without Ollama
3. Optional adapters for other providers

   * disabled by default
   * never required

All model outputs must be parsed into Pydantic schemas. Retry malformed structured output once, then use a safe deterministic fallback.

Do not let an LLM perform arithmetic, budget enforcement, distance calculation, or hard feasibility validation. Those must be deterministic.

## 7. Agentic workflow

Implement genuine cooperating components with clear responsibilities.

### 7.1 Intent and Constraint Agent

Convert user input into a structured `TripRequest` containing:

* origin
* destination
* start and end dates
* traveler count
* rooms or room assumptions
* total budget
* currency
* interests
* preferred pace
* transport preference
* accommodation preference
* food preferences
* accessibility constraints
* indoor/outdoor preference
* excluded activities
* free-text notes

Validate impossible or ambiguous combinations.

### 7.2 Destination Research Agent

Collect normalized candidate information from provider interfaces:

* destination overview
* attractions and points of interest
* categories and tags
* estimated duration
* coordinates
* approximate cost
* rating or popularity signal
* data source
* confidence
* opening-hour information when available

Use free/open sources where responsible:

* OpenStreetMap/Nominatim for geocoding
* Overpass API for public POIs
* Wikimedia or Wikipedia for destination context
* curated local datasets as fallback

All external calls must occur in the backend, not directly from the browser.

Respect public API usage policies:

* identifiable user agent
* caching
* rate limiting
* timeouts
* no duplicate requests
* graceful fallback

### 7.3 Transport Research Agent

Use a provider abstraction.

Default implementation:

* curated or synthetic estimated transport dataset
* route-distance-based estimate fallback
* transport modes such as flight, train, bus, and local transit
* explicit `is_estimate` field
* explicit source label

Do not claim live availability.

### 7.4 Accommodation Research Agent

Use a provider abstraction.

Default implementation:

* curated realistic accommodation dataset
* room occupancy assumptions
* nightly price estimate
* amenities
* area coordinates
* rating
* source and estimate label

Correctly calculate rooms, nights, taxes or contingency assumptions.

### 7.5 Weather Agent

Use Open-Meteo or another genuinely free weather source that does not require a paid key.

Return:

* date
* minimum and maximum temperature
* precipitation probability
* condition code and human-readable condition
* weather suitability tags
* source timestamp
* whether the date is within the forecast horizon

For dates outside the live forecast horizon, show historical/climatological guidance or an explicit “forecast unavailable” status. Never invent a live forecast for distant dates.

### 7.6 Geospatial Agent

Compute:

* Haversine distances
* activity clustering
* hotel-to-activity distance
* approximate daily travel burden
* geographic grouping by day

Optionally support an OSRM adapter, with a deterministic Haversine fallback.

Return coordinates in the backend response so the frontend never has to geocode itinerary text.

### 7.7 Optimization Agent

Implement a real multi-objective optimizer.

Use deterministic optimization, preferably Google OR-Tools CP-SAT, with a heuristic fallback.

Hard constraints:

* total cost must not exceed budget unless the system explicitly returns “no feasible plan”
* activities must fit inside daily time windows
* selected items must belong to the destination area
* avoid duplicate activities
* respect exclusions and accessibility constraints
* respect arrival and departure limitations
* respect maximum activities per day
* include meal and travel buffers

Soft objectives:

* preference match
* rating/popularity
* lower cost
* lower travel distance
* lower travel time
* weather suitability
* activity diversity
* balanced daily load
* accommodation quality
* confidence of source data

Implement configurable scoring weights.

Produce:

* selected plan
* at least two alternatives when feasible
* normalized total score
* score contribution breakdown
* rejected-option explanations
* binding constraints
* assumptions

Implement a baseline cheapest-first heuristic for research comparison.

### 7.8 Budget Agent

Calculate costs deterministically:

* transport
* accommodation
* activities
* estimated local transport
* estimated food
* contingency
* taxes or fees when modeled
* total
* remaining budget

Do not multiply room cost directly by traveler count. Use explicit occupancy and room-count assumptions.

Return warnings when a request is infeasible and provide actionable alternatives.

### 7.9 Itinerary Writer Agent

Transform validated structured itinerary data into concise, useful descriptions.

It must not alter:

* prices
* dates
* coordinates
* selections
* budget totals
* weather
* timings

Narrative content must remain grounded in structured facts.

### 7.10 Critic and Validation Agent

Perform final validation:

* budget consistency
* date consistency
* duplicate detection
* day capacity
* missing coordinates
* weather conflicts
* excessive travel
* unsupported claims
* empty days
* arrival/departure feasibility
* arithmetic reconciliation

The critic may request one revision cycle.

Final response must include validation status and warnings.

### 7.11 Revision Agent

Support follow-up requests using the previous structured itinerary rather than regenerating blindly.

Examples:

* reduce cost
* replace activity
* change pace
* add indoor activities
* account for rain
* prioritize food
* add a free day
* change accommodation tier

Record a revision history and explain what changed.

## 8. Backend API

Create a versioned API such as `/api/v1`.

Minimum endpoints:

```text
GET    /api/v1/health
POST   /api/v1/trips
GET    /api/v1/trips/{trip_id}
POST   /api/v1/trips/{trip_id}/revise
GET    /api/v1/trips/{trip_id}/events
DELETE /api/v1/trips/{trip_id}
GET    /api/v1/providers/status
GET    /api/v1/destinations/search
```

Use Server-Sent Events for real agent status.

Example event types:

```text
plan.started
agent.started
agent.progress
agent.completed
agent.failed
optimization.completed
validation.completed
plan.completed
plan.failed
```

Each event should include:

* event ID
* trip ID
* timestamp
* agent
* stage
* message
* progress percentage where meaningful
* safe metadata

Generate OpenAPI documentation with useful descriptions and examples.

## 9. Data model

Create strict schemas for at least:

* TripRequest
* TripPreferences
* TripPlan
* TripDay
* ScheduledActivity
* CandidateActivity
* TransportOption
* AccommodationOption
* WeatherForecast
* GeoPoint
* BudgetBreakdown
* ScoreBreakdown
* AgentEvent
* ValidationReport
* RevisionRequest
* RevisionRecord
* ProviderMetadata

Persist:

* trip request
* final plan
* alternatives
* agent events
* revision history
* provider metadata
* creation and update timestamps

Use SQLite by default.

## 10. Frontend experience

Design a genuinely polished product, not a single dark card.

### Pages

1. Landing page
2. Planner page
3. Planning progress page or integrated workspace
4. Itinerary results page
5. Saved trips page
6. Methodology/Explainability page
7. About/Research page
8. Friendly not-found and error pages

### Planner experience

Support both:

* structured form
* natural-language prompt

Required fields:

* origin
* destination
* dates
* budget
* travelers
* interests

Advanced expandable preferences:

* pace
* accommodation tier
* transport preference
* accessibility
* dietary preference
* indoor/outdoor preference
* exclusions

Use validated inputs and helpful errors.

### Real agent progress

Connect the UI to backend SSE.

Display actual states such as:

* Understanding constraints
* Researching transport
* Researching accommodation
* Discovering attractions
* Checking weather
* Clustering locations
* Optimizing schedule
* Verifying budget
* Writing itinerary
* Validating final plan

Show duration, completion state, and recoverable failures.

Do not simulate progress after the backend has already completed.

### Results experience

Show:

* concise trip summary
* assumptions and data freshness
* day-by-day timeline
* activity cards with time, duration, price, tags, coordinates, source, and rationale
* transport options
* accommodation recommendation
* weather by day
* interactive Leaflet map
* route or polyline
* budget visualization
* score explanation
* alternatives
* warnings
* “estimated data” labels
* revision assistant
* download/print itinerary
* local shareable JSON export

### Map requirements

* coordinates must come from the backend
* fit bounds correctly
* distinct markers per day
* numbered or categorized markers
* activity popups
* hotel marker
* route lines
* loading, empty, and error states
* accessible map description
* no direct Nominatim requests from the browser

### Visual design

Create a coherent design system:

* typography scale
* spacing system
* consistent cards
* accessible contrast
* subtle gradients
* restrained glass effects
* animations with reduced-motion support
* skeleton loading states
* light and dark themes
* responsive desktop, tablet, and mobile layouts
* keyboard navigation
* visible focus states
* semantic HTML
* ARIA only where needed

Avoid generic “AI purple gradient everywhere” design.

Use real icons from an open-source icon library instead of excessive emoji.

## 11. Research-grade optimization and evaluation

The repository must contain a reproducible experimental framework.

### Research question

Evaluate whether a coordinated multi-agent pipeline with deterministic multi-objective optimization creates more feasible and preference-aligned itineraries than simpler baselines.

### Systems to compare

1. Cheapest-first heuristic
2. Weighted ranking without scheduling optimization
3. Proposed multi-agent system with optimization and validation
4. Optional ablation without weather awareness
5. Optional ablation without geospatial clustering

### Metrics

Measure:

* budget violation rate
* itinerary feasibility rate
* preference coverage
* mean daily travel distance
* activity diversity
* weather-conflict rate
* number of validation errors
* average planning latency
* candidate-to-selection ratio
* percentage of complete itineraries
* estimated cost utilization
* deterministic reproducibility

Do not invent user satisfaction numbers.

If no real user study exists, explicitly state that limitation.

### Dataset

Create a reproducible benchmark dataset containing varied cases:

* low, medium, and high budgets
* solo, couple, family, and group travel
* 1-day through 7-day trips
* different interest combinations
* accessibility constraints
* rainy-weather scenarios
* infeasible budgets
* missing provider data
* multiple Indian destinations

Use synthetic cases transparently.

### Experiment artifacts

Create:

```text
research/experiments/run_benchmarks.py
research/experiments/run_ablations.py
research/results/*.csv
research/figures/*.png
research/paper/paper.tex
research/paper/references.bib
research/paper/README.md
```

Scripts must generate results and figures from actual runs.

Use fixed random seeds where randomness exists.

## 12. Research paper

Draft a formal paper titled approximately:

“An Explainable Multi-Agent Framework for Budget-Constrained Travel Itinerary Optimization”

Include:

1. Abstract
2. Keywords
3. Introduction
4. Problem statement
5. Related work
6. System architecture
7. Agent design
8. Optimization formulation
9. Data sources
10. Experimental methodology
11. Results
12. Ablation study
13. Discussion
14. Threats to validity
15. Ethical and privacy considerations
16. Limitations
17. Future work
18. Conclusion
19. References

Important:

* Never fabricate citations.
* Never fabricate experimental results.
* Add clearly marked placeholders where scholarly sources must be verified.
* Prefer primary research papers.
* Keep claims aligned with generated evidence.
* Include mathematical notation for the objective function and constraints.
* Generate architecture, agent-flow, and experiment-pipeline diagrams.
* Provide Mermaid source and publication-friendly exported figures where possible.

## 13. Testing

### Backend

Add tests for:

* request validation
* date calculations
* room calculations
* budget arithmetic
* scoring normalization
* Haversine distance
* clustering
* optimization feasibility
* infeasible requests
* weather fallback
* provider failure
* LLM malformed output
* critic validation
* revision behavior
* persistence
* SSE event order
* API endpoints

### Frontend

Add tests for:

* form validation
* API schema parsing
* loading and error states
* SSE progress rendering
* itinerary rendering
* budget chart
* map fallback
* revision form
* accessibility basics

### End-to-end

Add Playwright scenarios:

1. Create a normal trip.
2. Create an infeasible low-budget trip.
3. Receive streamed agent updates.
4. View map and budget.
5. Revise an itinerary.
6. Reload and retrieve a saved trip.
7. Export or print an itinerary.
8. Handle backend/provider failure gracefully.

Mock external providers during CI.

## 14. Performance and reliability

Implement:

* provider response caching
* deduplication
* request timeouts
* bounded retries with backoff
* cancellation
* concurrency limits
* database indexes where useful
* lazy loading for heavy frontend components
* map component code splitting if useful
* stable API response envelopes
* graceful degraded mode

Create a provider-status panel so the system can explain which data sources are operational.

## 15. Observability

Add:

* structured JSON-compatible backend logs
* request IDs
* trip IDs
* agent timing
* provider timing
* optimization timing
* failure categories
* health checks

Do not log prompts containing sensitive personal details unless explicitly configured for development.

## 16. Development and deployment

Provide:

* Windows PowerShell setup instructions
* Linux/macOS setup instructions
* Docker Compose for local execution
* backend and frontend production Dockerfiles
* `.env.example`
* database migration commands
* seed-data commands
* test commands
* lint commands
* build commands

Create GitHub Actions that:

* install dependencies
* lint frontend
* type-check frontend
* test frontend
* build frontend
* lint backend
* type-check backend
* test backend

Do not require paid infrastructure.

Document deployment options generically and do not promise that a provider’s free tier will remain available.

## 17. Documentation

Create or improve:

* README.md
* QUICKSTART.md
* CONTRIBUTING.md
* SECURITY.md
* DATA_SOURCES.md
* MODEL_CARD.md
* RESEARCH.md
* API documentation
* architecture diagrams
* agent sequence diagram
* data-flow diagram
* database ER diagram
* optimization explanation
* demo script
* five-minute presentation outline
* troubleshooting guide

The README must include:

* accurate feature status
* architecture
* screenshots placeholders
* local setup
* free data sources
* limitations
* estimated-data disclaimer
* testing instructions
* research section
* license

Do not claim unimplemented functionality.

## 18. Migration requirements

Refactor the existing application carefully.

Specifically fix:

* duplicated FastAPI request models
* repeated endpoints
* blocking HTTP calls in async code
* deprecated Pydantic `.dict()` calls
* hardcoded three-day duration
* missing destination/date fields in itinerary response
* direct browser geocoding
* missing coordinates
* weather dates outside forecast range
* map loading forever
* duplicate Goa coordinates for every day
* incorrect hotel multiplication
* malformed or unvalidated LLM responses
* raw Markdown displayed as plain text
* frontend `any` usage
* missing loading/error/empty states
* secret-handling risks
* inconsistent naming between `days` and `daily_plan`

Create one canonical API contract and migrate all components to it.

## 19. Acceptance criteria

The work is not complete until all of the following are true:

### Functional

* A user can create a trip with origin, destination, dates, travelers, budget, and interests.
* Trip duration is calculated from dates.
* Real backend agent events stream to the frontend.
* The optimizer returns a budget-feasible itinerary or a clear infeasibility result.
* Every scheduled activity has coordinates, date, time, duration, cost, source, and rationale.
* Weather is aligned to real itinerary dates or marked unavailable.
* The map renders hotel and activity markers without frontend geocoding.
* Budget totals reconcile exactly.
* The user can revise an existing itinerary.
* A trip can be persisted and reopened.
* The app works without a paid API.
* The app works without an LLM through deterministic fallback mode.

### Quality

* Backend tests pass.
* Frontend tests pass.
* End-to-end tests pass.
* Frontend production build passes.
* Backend starts without warnings caused by project code.
* Strict TypeScript passes.
* Ruff passes.
* Python type checking passes or all remaining exceptions are documented.
* No secret is tracked.
* No known placeholder is presented as implemented.
* README instructions work on Windows PowerShell.

### Research

* Benchmark scripts run.
* Results are written to CSV.
* Figures are generated from results.
* Baselines are implemented.
* At least one ablation study runs.
* The paper draft reflects actual implemented methods.
* No result or citation is fabricated.

## 20. Final completion response

When implementation is complete, return a final engineering report containing:

1. Executive summary
2. Architecture implemented
3. Agent workflow
4. Free data sources used
5. Main files created and modified
6. Commands executed
7. Tests and builds run
8. Exact pass/fail results
9. Research artifacts generated
10. Remaining limitations
11. Security review
12. How to run the system
13. How to run experiments
14. How to compile the paper
15. Recommended next improvements

Do not say “production ready” unless the acceptance criteria are satisfied.

Start now by auditing the repository. Do not immediately rewrite files before understanding the current implementation.
