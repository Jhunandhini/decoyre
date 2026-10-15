# Table subscriptions_legacy_stripe

Status: DEPRECATED | source: schemas/subscriptions_legacy_stripe.md | updated: 2024-11-05
Evidence: deprecated by decisions/adr-019-subscriptions-v3.md

# Table subscriptions_legacy_stripe

This is the table we use for the monthly MRR report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| region_code | varchar | Region |
| city | varchar | City name |
| is_test | boolean | Test row flag |
| status | varchar | Lifecycle status |
| gross_amount | decimal | Amount after tax |
| created_at | timestamp | Row creation time |
| pincode | varchar | Postal code |
| customer_id | bigint | FK to customers |
| tags | jsonb | Arbitrary tags |
| deleted_at | timestamp | Soft delete time |
| country | char(2) | Country code |
| store_id | int | FK to stores |
| tax_amount | decimal | Tax amount |
| external_ref | varchar | Reference in upstream system |
| updated_at | timestamp | Last update time |
| batch_id | bigint | Load batch |
| priority | int | Priority 1-5 |
| created_by | varchar | User or service that created the row |
| plan_period | varchar | Plan period |
| net_amount | decimal | Amount before tax |
| notes | text | Free text notes |
| source_system | varchar | Ingestion source |
| users_n | int | Number of users |
| version | int | Row version |
