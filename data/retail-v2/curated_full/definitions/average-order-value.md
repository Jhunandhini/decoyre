# AOV - analytics definition

Status: CURRENT | source: wiki/finance/aov-analytics-definition.md | updated: 2025-04-20
Evidence: declared authoritative by decisions/adr-020-average-order-value.md

# AOV - analytics definition

Owner: finance analytics.

`AOV = SUM(net_amount) / COUNT(DISTINCT order_id) WHERE status = 'completed'`

Only completed orders are counted; cancelled orders are excluded.

## Additional rules found in other documents

- From this quarter on, everyone should follow the finance team's page "AOV - analytics definition". Please ignore the 2023 analytics write-up "How we calculate average order value" when building reports. (from decisions/adr-020-average-order-value.md)

## History (do not use)

- wiki/how-we-calculate-average-order-value.md is DEPRECATED, superseded by wiki/finance/aov-analytics-definition.md
