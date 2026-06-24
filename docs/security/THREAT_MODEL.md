# Threat Model

Protected assets:

- anonymous trip records
- event history
- database credentials
- deployment environment variables

Controls:

- anonymous owner token hashing
- no global public trip list
- bounded request sizes
- rate limiting
- strict production CORS
- no committed secrets
- readiness health that does not expose internals
