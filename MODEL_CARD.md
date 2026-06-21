# Model Card

## Default Narrative Provider

Provider: `TemplateLLMProvider`

Type: deterministic template fallback

Requires paid service: no

Can alter prices, dates, coordinates, or selections: no

## Optional Local LLM Direction

The backend configuration includes Ollama fields:

- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`

The currently implemented default path does not require Ollama. A future adapter can implement the `LLMProvider` protocol while preserving deterministic validation.
