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
| status | varchar | Lifecycle status |
| updated_at | timestamp | Last update time |
| country | char(2) | Country code |
| city | varchar | City name |
| tax_amount | decimal | Tax amount |
| customer_id | bigint | FK to customers |
| deleted_at | timestamp | Soft delete time |
| priority | int | Priority 1-5 |
| batch_id | bigint | Load batch |
| source_system | varchar | Ingestion source |
| net_amount | decimal | Amount before tax |
| region_code | varchar | Region |
| is_test | boolean | Test row flag |
| notes | text | Free text notes |
| version | int | Row version |
| promo_amt | decimal | Promotion amount |
| partner_id | int | Partner FK |
| channel_code | char(2) | Two letter channel code |
| pincode | varchar | Postal code |
| created_by | varchar | User or service that created the row |
| created_at | timestamp | Row creation time |
| gross_amount | decimal | Amount after tax |
| tags | jsonb | Arbitrary tags |
| store_id | int | FK to stores |
