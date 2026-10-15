# Table orders

Status: STALE | source: schemas/orders.md | updated: 2024-11-05
Evidence: older than schemas/orders_v2.md

# Table orders

Original orders table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| notes | text | Free text notes |
| region_code | varchar | Region |
| gross_amount | decimal | Amount after tax |
| tax_amount | decimal | Tax amount |
| pincode | varchar | Postal code |
| country | char(2) | Country code |
| created_by | varchar | User or service that created the row |
| version | int | Row version |
| updated_at | timestamp | Last update time |
| status | varchar | Lifecycle status |
