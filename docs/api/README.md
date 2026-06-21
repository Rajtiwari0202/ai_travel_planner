# API

Base path: `/api/v1`

## Create Trip

`POST /api/v1/trips`

Returns `202 Accepted` with `trip_id` and `events_url`. Planning runs in a background task and persists events and the final plan.

## Event Stream

`GET /api/v1/trips/{trip_id}/events`

Uses Server-Sent Events. Event names include:

- `plan.started`
- `agent.started`
- `agent.completed`
- `optimization.completed`
- `validation.completed`
- `plan.completed`
- `plan.failed`

## Retrieve Trip

`GET /api/v1/trips/{trip_id}`

Returns the saved request and plan when available.
