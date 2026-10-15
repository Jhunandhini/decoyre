# DAU - product analytics definition

Status: CURRENT | source: wiki/finance/dau-product-analytics-definition.md | updated: 2025-03-03
Evidence: declared authoritative by decisions/adr-015-daily-active-users.md

# DAU - product analytics definition

Owner: finance analytics.

`DAU = distinct users with at least one session_event of type 'core_action' in the day`

Background API calls from integrations no longer count as activity.

## Additional rules found in other documents

- This decision replaces the old "How we count daily active users" wiki page. The authoritative definition now lives in the page "DAU - product analytics definition". (from decisions/adr-015-daily-active-users.md)

## History (do not use)

- wiki/how-we-count-daily-active-users.md is DEPRECATED, superseded by wiki/finance/dau-product-analytics-definition.md
