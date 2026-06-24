# Error Model

The API returns standard HTTP status codes with a JSON `detail` field.

- `400`: invalid request shape or validation failure.
- `404`: trip not found or not owned by the anonymous session.
- `413`: request body too large.
- `429`: public demo rate limit exceeded.
- `503`: readiness failed because the database is unavailable.

Production responses must not include stack traces, secrets, database URLs, or internal paths.
