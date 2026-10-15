# Table orders_v2 (current)

Authoritative orders table; source of the monthly sales report. Do not use orders_legacy_pos (deprecated), orders (deprecated) or orders_staging (ingestion only).

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| deleted_at | timestamp | Soft delete time |
| tax_amount | decimal | Tax amount |
| country | char(2) | Country code |
| is_test | boolean | Test row flag |
| store_id | int | FK to stores |
| created_at | timestamp | Row creation time |
| batch_id | bigint | Load batch |
| partner_id | int | Partner FK |
| customer_id | bigint | FK to customers |
| city | varchar | City name |
| currency | char(3) | ISO currency |
| created_by | varchar | User or service that created the row |
| notes | text | Free text notes |
| net_amount | decimal | Amount before tax |
| status | varchar | Lifecycle status |
| external_ref | varchar | Reference in upstream system |
| version | int | Row version |
| source_system | varchar | Ingestion source |
| priority | int | Priority 1-5 |
| updated_at | timestamp | Last update time |
| sales_channel | varchar | Channel where the order was placed: app, web, store |
| pincode | varchar | Postal code |
| gross_amount | decimal | Amount after tax |
| discount_total | decimal | Total discount applied to the order |
