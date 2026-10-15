# Table subscriptions_v3

Status: CURRENT | source: schemas/subscriptions_v3.md | updated: 2025-01-20
Evidence: latest dated document in topic

# Table subscriptions_v3

Cleaned subscriptions table, one row per subscription. Deduplicated.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| pincode | varchar | Postal code |
| batch_id | bigint | Load batch |
| region_code | varchar | Region |
| version | int | Row version |
| partner_id | int | Partner FK |
| created_at | timestamp | Row creation time |
| status | varchar | Lifecycle status |
| store_id | int | FK to stores |
| external_ref | varchar | Reference in upstream system |
| source_system | varchar | Ingestion source |
| country | char(2) | Country code |
| tags | jsonb | Arbitrary tags |
| priority | int | Priority 1-5 |
| gross_amount | decimal | Amount after tax |
| net_amount | decimal | Amount before tax |
| created_by | varchar | User or service that created the row |
| notes | text | Free text notes |
| tax_amount | decimal | Tax amount |
| deleted_at | timestamp | Soft delete time |
| city | varchar | City name |
| is_test | boolean | Test row flag |
| billing_interval | varchar | monthly or annual billing interval |
| updated_at | timestamp | Last update time |
| seat_count | int | Number of seats purchased |
