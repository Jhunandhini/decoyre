# Table subscriptions_v3

Status: CURRENT | source: schemas/subscriptions_v3.md | updated: 2025-01-20
Evidence: declared authoritative by decisions/adr-019-subscriptions-v3.md

# Table subscriptions_v3

Cleaned subscriptions table, one row per subscription. Deduplicated.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| tags | jsonb | Arbitrary tags |
| store_id | int | FK to stores |
| deleted_at | timestamp | Soft delete time |
| net_amount | decimal | Amount before tax |
| currency | char(3) | ISO currency |
| created_at | timestamp | Row creation time |
| version | int | Row version |
| pincode | varchar | Postal code |
| priority | int | Priority 1-5 |
| external_ref | varchar | Reference in upstream system |
| created_by | varchar | User or service that created the row |
| is_test | boolean | Test row flag |
| notes | text | Free text notes |
| tax_amount | decimal | Tax amount |
| updated_at | timestamp | Last update time |
| batch_id | bigint | Load batch |
| country | char(2) | Country code |
| seat_count | int | Number of seats purchased |
| partner_id | int | Partner FK |
| city | varchar | City name |
| gross_amount | decimal | Amount after tax |
| region_code | varchar | Region |
| billing_interval | varchar | monthly or annual billing interval |
| status | varchar | Lifecycle status |
