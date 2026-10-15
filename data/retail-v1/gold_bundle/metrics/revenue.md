# Revenue

Status: current (since 2025-05-12, decisions/adr-014-revenue.md)

`revenue = SUM(net_amount) - SUM(refund_amount)`

Net of refunds. GST and shipping fees are excluded because net_amount is stored pre-tax.

The 2023 definition in wiki/how-we-calculate-revenue.md is deprecated.
