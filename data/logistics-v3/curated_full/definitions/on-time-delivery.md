# OTD - operations definition

Status: CURRENT | source: wiki/finance/otd-operations-definition.md | updated: 2025-01-19
Evidence: declared authoritative by decisions/adr-021-on-time-delivery.md

# OTD - operations definition

Owner: finance analytics.

`on_time = delivered_at <= promised_window_end + 30 minutes grace`

We now compare against the promised_window_end timestamp with a 30 minute grace period.

## History (do not use)

- wiki/how-we-calculate-on-time-delivery.md is DEPRECATED, superseded by wiki/finance/otd-operations-definition.md
