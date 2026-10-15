---
title: Table orders
topic: orders-tables
updated: 2024-11-05
owner: data-eng
---

# Table orders

Original orders table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| gross_amount | decimal | Amount after tax |
| created_by | varchar | User or service that created the row |
| pincode | varchar | Postal code |
| tags | jsonb | Arbitrary tags |
| country | char(2) | Country code |
| region_code | varchar | Region |
| created_at | timestamp | Row creation time |
| source_system | varchar | Ingestion source |
| updated_at | timestamp | Last update time |
| is_test | boolean | Test row flag |
