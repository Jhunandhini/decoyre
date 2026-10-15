---
title: Table shipments_v2
topic: shipments-tables
updated: 2025-01-20
owner: data-eng
---

# Table shipments_v2

Cleaned shipments table, one row per shipment. Deduplicated.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| version | int | Row version |
| country | char(2) | Country code |
| deleted_at | timestamp | Soft delete time |
| priority | int | Priority 1-5 |
| notes | text | Free text notes |
| city | varchar | City name |
| source_system | varchar | Ingestion source |
| created_by | varchar | User or service that created the row |
| created_at | timestamp | Row creation time |
| net_amount | decimal | Amount before tax |
| customer_id | bigint | FK to customers |
| tags | jsonb | Arbitrary tags |
| batch_id | bigint | Load batch |
| partner_id | int | Partner FK |
| currency | char(3) | ISO currency |
| cod_amount | decimal | Cash on delivery amount to collect |
| tax_amount | decimal | Tax amount |
| status | varchar | Lifecycle status |
| store_id | int | FK to stores |
| updated_at | timestamp | Last update time |
| vehicle_class | varchar | Vehicle type: bike, van, 14ft truck |
| is_test | boolean | Test row flag |
| pincode | varchar | Postal code |
| region_code | varchar | Region |
