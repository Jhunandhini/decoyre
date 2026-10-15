# Table orders_legacy_pos

Status: STALE | source: schemas/orders_legacy_pos.md | updated: 2024-11-05
Evidence: older than schemas/orders_v2.md

# Table orders_legacy_pos

This is the table we use for the monthly sales report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| region_code | varchar | Region |
| store_id | int | FK to stores |
| source_system | varchar | Ingestion source |
| priority | int | Priority 1-5 |
| external_ref | varchar | Reference in upstream system |
| pincode | varchar | Postal code |
| created_by | varchar | User or service that created the row |
| customer_id | bigint | FK to customers |
| country | char(2) | Country code |
| is_test | boolean | Test row flag |
| tags | jsonb | Arbitrary tags |
| batch_id | bigint | Load batch |
| created_at | timestamp | Row creation time |
| version | int | Row version |
| currency | char(3) | ISO currency |
| updated_at | timestamp | Last update time |
| city | varchar | City name |
| channel_code | char(2) | Two letter channel code |
| gross_amount | decimal | Amount after tax |
| deleted_at | timestamp | Soft delete time |
| notes | text | Free text notes |
| promo_amt | decimal | Promotion amount |
| status | varchar | Lifecycle status |
| tax_amount | decimal | Tax amount |
