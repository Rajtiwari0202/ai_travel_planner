## TravelAgenticAI Frontend

This is the React + Tailwind frontend for the multi-agent travel planner.

It talks to the FastAPI backend at `http://localhost:8000` and renders:

- Trip planner form
- Live agent activity
- Narrative itinerary results
- Map and budget visuals
- Saved trip history

## Running The Frontend

From the `frontend` folder:

```bash
npm install
npm run dev
```

Then open `http://127.0.0.1:5173` in your browser.

Make sure the backend is also running on `http://localhost:8000`.
