# Table shipments

Status: STALE | source: schemas/shipments.md | updated: 2024-11-05
Evidence: older than schemas/shipments_v2.md

# Table shipments

Original shipments table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| country | char(2) | Country code |
| partner_id | int | Partner FK |
| external_ref | varchar | Reference in upstream system |
| status | varchar | Lifecycle status |
| region_code | varchar | Region |
| customer_id | bigint | FK to customers |
| priority | int | Priority 1-5 |
| store_id | int | FK to stores |
| pincode | varchar | Postal code |
| city | varchar | City name |
