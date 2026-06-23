# Frontend Architecture

The frontend is a Vite React TypeScript app.

Key areas:

- `src/app/App.tsx`: routing and top-level shell.
- `src/features/planner`: planner form, workspace, provider status panel.
- `src/features/agents`: streamed progress timeline.
- `src/features/itinerary`: itinerary rendering.
- `src/features/budget`: budget visualization.
- `src/features/map`: Leaflet activity map.
- `src/services/api.ts`: typed API calls, anonymous session token, readiness retry.

The browser stores a random anonymous session token in local storage. Only a hash of that token is stored server-side.
