---
title: Table orders_staging
topic: orders-tables
updated: 2024-11-05
owner: data-eng
---

# Table orders_staging

Intermediate staging table loaded hourly by the ingestion job. Not for reporting.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| tax_amount | decimal | Tax amount |
| created_by | varchar | User or service that created the row |
| country | char(2) | Country code |
| gross_amount | decimal | Amount after tax |
| region_code | varchar | Region |
| notes | text | Free text notes |
| partner_id | int | Partner FK |
| net_amount | decimal | Amount before tax |
| is_test | boolean | Test row flag |
| created_at | timestamp | Row creation time |
| city | varchar | City name |
| external_ref | varchar | Reference in upstream system |
