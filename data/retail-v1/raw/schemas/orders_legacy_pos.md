---
title: Table orders_legacy_pos
topic: orders-tables
updated: 2024-11-05
owner: data-eng
---

# Table orders_legacy_pos

This is the table we use for the monthly sales report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| city | varchar | City name |
| net_amount | decimal | Amount before tax |
| source_system | varchar | Ingestion source |
| currency | char(3) | ISO currency |
| status | varchar | Lifecycle status |
| notes | text | Free text notes |
| updated_at | timestamp | Last update time |
| gross_amount | decimal | Amount after tax |
| country | char(2) | Country code |
| deleted_at | timestamp | Soft delete time |
| tax_amount | decimal | Tax amount |
| is_test | boolean | Test row flag |
| created_at | timestamp | Row creation time |
| store_id | int | FK to stores |
| priority | int | Priority 1-5 |
| partner_id | int | Partner FK |
| promo_amt | decimal | Promotion amount |
| version | int | Row version |
| channel_code | char(2) | Two letter channel code |
| pincode | varchar | Postal code |
| created_by | varchar | User or service that created the row |
| customer_id | bigint | FK to customers |
| region_code | varchar | Region |
| batch_id | bigint | Load batch |
