# DAU - product analytics definition

Status: CURRENT | source: wiki/finance/dau-product-analytics-definition.md | updated: 2025-06-12
Evidence: declared authoritative by decisions/adr-013-daily-active-users.md

# DAU - product analytics definition

Owner: finance analytics.

`DAU = distinct users with at least one session_event of type 'core_action' in the day`

Background API calls from integrations no longer count as activity.

## Additional rules found in other documents

- From this quarter on, everyone should follow the finance team's page "DAU - product analytics definition". Please ignore the 2023 analytics write-up "How we count daily active users" when building reports. (from decisions/adr-013-daily-active-users.md)

## History (do not use)

- wiki/how-we-count-daily-active-users.md is DEPRECATED, superseded by wiki/finance/dau-product-analytics-definition.md
