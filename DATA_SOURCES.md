# Data Sources

Default data is local and transparent:

- Destination profiles: curated local demonstration dataset
- Activity candidates: curated/open-data inspired POI coordinates
- Transport: distance-based estimated model
- Accommodation: curated estimated room-price model
- Weather: fallback seasonal guidance by default
- Optional live weather: Open-Meteo when `ENABLE_LIVE_WEATHER=true`

No default provider returns live booking inventory.

## Labels

- `estimate`: calculated estimate, not live availability
- `open_data`: public/open-data inspired source
- `fallback`: deterministic fallback when live provider is disabled or unavailable
- `synthetic`: generated fallback when destination is not in the bundled dataset
- `live`: real provider response, only when enabled
