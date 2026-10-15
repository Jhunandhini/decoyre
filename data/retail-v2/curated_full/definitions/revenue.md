# Revenue - finance definition

Status: CURRENT | source: wiki/finance/revenue-finance-definition.md | updated: 2025-02-07
Evidence: declared authoritative by decisions/adr-018-revenue.md

# Revenue - finance definition

Owner: finance analytics.

`revenue = SUM(net_amount) - SUM(refund_amount)`

Net of refunds. GST and shipping fees are excluded because net_amount is stored pre-tax.

## Additional rules found in other documents

- Finance and the board pack reported different revenue numbers because one included GST. (from decisions/adr-018-revenue.md)
- From this quarter on, everyone should follow the finance team's page "Revenue - finance definition". Please ignore the 2023 analytics write-up "How we calculate revenue" when building reports. (from decisions/adr-018-revenue.md)

## History (do not use)

- wiki/how-we-calculate-revenue.md is DEPRECATED, superseded by wiki/finance/revenue-finance-definition.md
