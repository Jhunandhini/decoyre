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
| version | int | Row version |
| pincode | varchar | Postal code |
| external_ref | varchar | Reference in upstream system |
| store_id | int | FK to stores |
| tags | jsonb | Arbitrary tags |
| net_amount | decimal | Amount before tax |
| country | char(2) | Country code |
| created_by | varchar | User or service that created the row |
| created_at | timestamp | Row creation time |
| customer_id | bigint | FK to customers |
| source_system | varchar | Ingestion source |
| deleted_at | timestamp | Soft delete time |
