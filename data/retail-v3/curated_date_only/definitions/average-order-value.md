# AOV - analytics definition

Status: CURRENT | source: wiki/finance/aov-analytics-definition.md | updated: 2025-04-03
Evidence: latest dated document in topic

# AOV - analytics definition

Owner: finance analytics.

`AOV = SUM(net_amount) / COUNT(DISTINCT order_id) WHERE status = 'completed'`

Only completed orders are counted; cancelled orders are excluded.

## Additional rules found in other documents

- This decision replaces the old "How we calculate average order value" wiki page. The authoritative definition now lives in the page "AOV - analytics definition". (from decisions/adr-019-average-order-value.md)

## History (do not use)

- wiki/how-we-calculate-average-order-value.md is STALE, superseded by wiki/finance/aov-analytics-definition.md
