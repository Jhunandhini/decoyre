# Table subscriptions

Status: STALE | source: schemas/subscriptions.md | updated: 2024-11-05
Evidence: not the declared current table

# Table subscriptions

Original subscriptions table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| notes | text | Free text notes |
| tags | jsonb | Arbitrary tags |
| region_code | varchar | Region |
| created_by | varchar | User or service that created the row |
| updated_at | timestamp | Last update time |
| currency | char(3) | ISO currency |
| batch_id | bigint | Load batch |
| country | char(2) | Country code |
| partner_id | int | Partner FK |
| is_test | boolean | Test row flag |
