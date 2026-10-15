# Table shipments

Status: STALE | source: schemas/shipments.md | updated: 2024-11-05
Evidence: not the declared current table

# Table shipments

Original shipments table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| source_system | varchar | Ingestion source |
| batch_id | bigint | Load batch |
| city | varchar | City name |
| store_id | int | FK to stores |
| created_by | varchar | User or service that created the row |
| external_ref | varchar | Reference in upstream system |
| gross_amount | decimal | Amount after tax |
| currency | char(3) | ISO currency |
| is_test | boolean | Test row flag |
| pincode | varchar | Postal code |
