# Table orders_v2

Status: CURRENT | source: schemas/orders_v2.md | updated: 2025-01-20
Evidence: declared authoritative by decisions/adr-019-orders-v2.md

# Table orders_v2

Cleaned orders table, one row per order. Deduplicated.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| currency | char(3) | ISO currency |
| pincode | varchar | Postal code |
| store_id | int | FK to stores |
| region_code | varchar | Region |
| partner_id | int | Partner FK |
| created_by | varchar | User or service that created the row |
| updated_at | timestamp | Last update time |
| gross_amount | decimal | Amount after tax |
| net_amount | decimal | Amount before tax |
| deleted_at | timestamp | Soft delete time |
| country | char(2) | Country code |
| batch_id | bigint | Load batch |
| external_ref | varchar | Reference in upstream system |
| created_at | timestamp | Row creation time |
| priority | int | Priority 1-5 |
| status | varchar | Lifecycle status |
| discount_total | decimal | Total discount applied to the order |
| is_test | boolean | Test row flag |
| customer_id | bigint | FK to customers |
| tax_amount | decimal | Tax amount |
| sales_channel | varchar | Channel where the order was placed: app, web, store |
| version | int | Row version |
| city | varchar | City name |
| tags | jsonb | Arbitrary tags |
