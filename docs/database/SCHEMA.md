# Database Schema

Tables:

- `trip_records`
  - `trip_id`
  - `status`
  - `owner_hash`
  - `request_json`
  - `plan_json`
  - `created_at`
  - `updated_at`
- `agent_event_records`
  - `id`
  - `trip_id`
  - `sequence`
  - `event_id`
  - `event_json`
  - `created_at`

Indexes support trip status, anonymous ownership, and ordered event replay.
