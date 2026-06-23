# Logging

The backend emits standard application logs. Production logs should include request ID, trip ID where available, stage, duration, and sanitized error category.

Never log:

- full database URLs
- anonymous session tokens
- provider secrets
- stack traces in public responses
