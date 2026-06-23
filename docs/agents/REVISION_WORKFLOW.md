# Revision Workflow

Revision accepts a bounded instruction string. The backend updates structured preferences where possible, replans, compares the new itinerary with the previous version, and appends a `RevisionRecord`.

Supported deterministic signals include:

- adventure preference
- indoor/rain preference
- updated budget number

Unsupported instructions trigger a safe replan with the request recorded in revision history.
