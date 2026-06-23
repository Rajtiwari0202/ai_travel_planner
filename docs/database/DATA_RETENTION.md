# Data Retention

The public demo stores anonymous trip data only for a configurable period.

Variable:

```text
ANONYMOUS_TRIP_TTL_DAYS=7
```

Cleanup runs opportunistically at startup. Do not store passports, payment data, or booking credentials in this demo.
