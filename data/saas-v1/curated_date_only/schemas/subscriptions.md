# Table subscriptions

Status: STALE | source: schemas/subscriptions.md | updated: 2024-11-05
Evidence: older than schemas/subscriptions_v3.md

# Table subscriptions

Original subscriptions table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| region_code | varchar | Region |
| partner_id | int | Partner FK |
| is_test | boolean | Test row flag |
| gross_amount | decimal | Amount after tax |
| status | varchar | Lifecycle status |
| updated_at | timestamp | Last update time |
| tags | jsonb | Arbitrary tags |
| created_by | varchar | User or service that created the row |
| version | int | Row version |
| customer_id | bigint | FK to customers |
