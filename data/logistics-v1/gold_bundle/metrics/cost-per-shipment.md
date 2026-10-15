# Cost per shipment

Status: current (since 2025-04-15, decisions/adr-018-cost-per-shipment.md)

`cost_per_shipment = (fuel_cost + driver_cost + toll_cost) / delivered_shipments`

Only delivered_shipments are in the denominator.

The 2023 definition in wiki/how-we-calculate-cost-per-shipment.md is deprecated.
