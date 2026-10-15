# Table orders_v2 (current)

Authoritative orders table; source of the monthly sales report. Do not use orders_legacy_pos (deprecated), orders (deprecated) or orders_staging (ingestion only).

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| updated_at | timestamp | Last update time |
| status | varchar | Lifecycle status |
| currency | char(3) | ISO currency |
| store_id | int | FK to stores |
| source_system | varchar | Ingestion source |
| version | int | Row version |
| net_amount | decimal | Amount before tax |
| tax_amount | decimal | Tax amount |
| gross_amount | decimal | Amount after tax |
| batch_id | bigint | Load batch |
| priority | int | Priority 1-5 |
| created_at | timestamp | Row creation time |
| notes | text | Free text notes |
| created_by | varchar | User or service that created the row |
| city | varchar | City name |
| partner_id | int | Partner FK |
| external_ref | varchar | Reference in upstream system |
| country | char(2) | Country code |
| is_test | boolean | Test row flag |
| deleted_at | timestamp | Soft delete time |
| region_code | varchar | Region |
| pincode | varchar | Postal code |
| discount_total | decimal | Total discount applied to the order |
| sales_channel | varchar | Channel where the order was placed: app, web, store |
