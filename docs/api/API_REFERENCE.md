# API Reference

Base path: `/api/v1`

- `GET /health`
- `GET /health/live`
- `GET /health/ready`
- `GET /version`
- `POST /trips`
- `GET /trips`
- `GET /trips/{trip_id}`
- `GET /trips/{trip_id}/events`
- `POST /trips/{trip_id}/revise`
- `DELETE /trips/{trip_id}`
- `GET /providers/status`
- `GET /destinations/search`

Public demo clients should send `X-Anonymous-Session` on fetch requests. SSE passes the same token as a `session` query parameter because native `EventSource` cannot set custom headers.
