---
title: Table shipments_staging
topic: shipments-tables
updated: 2024-11-05
owner: data-eng
---

# Table shipments_staging

Intermediate staging table loaded hourly by the ingestion job. Not for reporting.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| deleted_at | timestamp | Soft delete time |
| net_amount | decimal | Amount before tax |
| source_system | varchar | Ingestion source |
| updated_at | timestamp | Last update time |
| store_id | int | FK to stores |
| version | int | Row version |
| created_at | timestamp | Row creation time |
| pincode | varchar | Postal code |
| country | char(2) | Country code |
| customer_id | bigint | FK to customers |
| priority | int | Priority 1-5 |
| status | varchar | Lifecycle status |
