# Table subscriptions_legacy_stripe

Status: STALE | source: schemas/subscriptions_legacy_stripe.md | updated: 2024-11-05
Evidence: older than schemas/subscriptions_v3.md

# Table subscriptions_legacy_stripe

This is the table we use for the monthly MRR report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| pincode | varchar | Postal code |
| updated_at | timestamp | Last update time |
| city | varchar | City name |
| created_at | timestamp | Row creation time |
| batch_id | bigint | Load batch |
| customer_id | bigint | FK to customers |
| status | varchar | Lifecycle status |
| source_system | varchar | Ingestion source |
| gross_amount | decimal | Amount after tax |
| store_id | int | FK to stores |
| deleted_at | timestamp | Soft delete time |
| currency | char(3) | ISO currency |
| region_code | varchar | Region |
| net_amount | decimal | Amount before tax |
| partner_id | int | Partner FK |
| tags | jsonb | Arbitrary tags |
| version | int | Row version |
| tax_amount | decimal | Tax amount |
| plan_period | varchar | Plan period |
| priority | int | Priority 1-5 |
| external_ref | varchar | Reference in upstream system |
| users_n | int | Number of users |
| is_test | boolean | Test row flag |
| created_by | varchar | User or service that created the row |
