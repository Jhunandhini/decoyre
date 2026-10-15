---
title: AOV - analytics definition
topic: average-order-value
updated: 2025-04-03
owner: finance
---

# AOV - analytics definition

Owner: finance analytics.

`AOV = SUM(net_amount) / COUNT(DISTINCT order_id) WHERE status = 'completed'`

Only completed orders are counted; cancelled orders are excluded.
