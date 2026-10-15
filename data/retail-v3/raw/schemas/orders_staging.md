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
| version | int | Row version |
| source_system | varchar | Ingestion source |
| is_test | boolean | Test row flag |
| batch_id | bigint | Load batch |
| region_code | varchar | Region |
| priority | int | Priority 1-5 |
| currency | char(3) | ISO currency |
| external_ref | varchar | Reference in upstream system |
| updated_at | timestamp | Last update time |
| customer_id | bigint | FK to customers |
| status | varchar | Lifecycle status |
| deleted_at | timestamp | Soft delete time |
