# Average order value (aov)

Status: current (since 2025-04-20, decisions/adr-020-average-order-value.md)

`AOV = SUM(net_amount) / COUNT(DISTINCT order_id) WHERE status = 'completed'`

Only completed orders are counted; cancelled orders are excluded.

The 2023 definition in wiki/how-we-calculate-average-order-value.md is deprecated.
