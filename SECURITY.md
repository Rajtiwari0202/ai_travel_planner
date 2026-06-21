# Security

## Supported Model

This local demo is not a hosted service. Security reports should focus on repository code, local API behavior, dependency risks, and accidental data exposure.

## Secrets

- Do not commit `.env` files.
- `.env.example` contains placeholders only.
- Optional paid or local model providers must be disabled by default.
- Logs should not include secret values.

## Local Data

Trip requests and generated plans are stored in SQLite by default. Treat that database as local user data and do not commit it.

## Network Calls

Live weather is disabled by default. When enabled, provider calls use timeouts and transparent source labels.
