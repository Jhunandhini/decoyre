# Table orders

Status: STALE | source: schemas/orders.md | updated: 2024-11-05
Evidence: not the declared current table

# Table orders

Original orders table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| customer_id | bigint | FK to customers |
| deleted_at | timestamp | Soft delete time |
| version | int | Row version |
| priority | int | Priority 1-5 |
| city | varchar | City name |
| tax_amount | decimal | Tax amount |
| region_code | varchar | Region |
| external_ref | varchar | Reference in upstream system |
| created_at | timestamp | Row creation time |
| is_test | boolean | Test row flag |
