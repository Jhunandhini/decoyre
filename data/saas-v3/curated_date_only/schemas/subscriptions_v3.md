# Table subscriptions_v3

Status: CURRENT | source: schemas/subscriptions_v3.md | updated: 2025-01-20
Evidence: latest dated document in topic

# Table subscriptions_v3

Cleaned subscriptions table, one row per subscription. Deduplicated.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| created_by | varchar | User or service that created the row |
| gross_amount | decimal | Amount after tax |
| version | int | Row version |
| notes | text | Free text notes |
| tax_amount | decimal | Tax amount |
| customer_id | bigint | FK to customers |
| status | varchar | Lifecycle status |
| city | varchar | City name |
| priority | int | Priority 1-5 |
| pincode | varchar | Postal code |
| country | char(2) | Country code |
| deleted_at | timestamp | Soft delete time |
| external_ref | varchar | Reference in upstream system |
| created_at | timestamp | Row creation time |
| region_code | varchar | Region |
| billing_interval | varchar | monthly or annual billing interval |
| batch_id | bigint | Load batch |
| updated_at | timestamp | Last update time |
| seat_count | int | Number of seats purchased |
| tags | jsonb | Arbitrary tags |
| is_test | boolean | Test row flag |
| store_id | int | FK to stores |
| source_system | varchar | Ingestion source |
| partner_id | int | Partner FK |
