# How we calculate average order value

Status: CURRENT | source: wiki/how-we-calculate-average-order-value.md | updated: 2025-12-12
Evidence: latest dated document in topic

> Note: this page is deprecated, see wiki/finance/aov-analytics-definition.md.

# How we calculate average order value

This page explains how we calculate average order value (AOV) at Kovai Mart.

## Formula

`AOV = SUM(gross_amount) / COUNT(session_id)`

Average order value divides gross sales by the number of shopping sessions.

## Where it is used

Weekly business review and the leadership dashboard.

## Changelog

- 2025-12-12: fixed a typo in the heading.

## Additional rules found in other documents

- This decision replaces the old "How we calculate average order value" wiki page. The authoritative definition now lives in the page "AOV - analytics definition". (from decisions/adr-016-average-order-value.md)

## History (do not use)

- wiki/finance/aov-analytics-definition.md is STALE, superseded by wiki/how-we-calculate-average-order-value.md
