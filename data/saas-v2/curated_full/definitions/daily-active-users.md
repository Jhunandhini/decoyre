# DAU - product analytics definition

Status: CURRENT | source: wiki/finance/dau-product-analytics-definition.md | updated: 2025-04-01
Evidence: declared authoritative by decisions/adr-015-daily-active-users.md

# DAU - product analytics definition

Owner: finance analytics.

`DAU = distinct users with at least one session_event of type 'core_action' in the day`

Background API calls from integrations no longer count as activity.

## History (do not use)

- wiki/how-we-count-daily-active-users.md is DEPRECATED, superseded by wiki/finance/dau-product-analytics-definition.md
