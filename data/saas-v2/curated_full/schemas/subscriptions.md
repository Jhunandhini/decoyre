# Table subscriptions

Status: STALE | source: schemas/subscriptions.md | updated: 2024-11-05
Evidence: not the declared current table

# Table subscriptions

Original subscriptions table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| version | int | Row version |
| gross_amount | decimal | Amount after tax |
| priority | int | Priority 1-5 |
| created_by | varchar | User or service that created the row |
| tags | jsonb | Arbitrary tags |
| batch_id | bigint | Load batch |
| pincode | varchar | Postal code |
| country | char(2) | Country code |
| updated_at | timestamp | Last update time |
| store_id | int | FK to stores |
