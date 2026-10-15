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
| net_amount | decimal | Amount before tax |
| gross_amount | decimal | Amount after tax |
| version | int | Row version |
| status | varchar | Lifecycle status |
| city | varchar | City name |
| customer_id | bigint | FK to customers |
| country | char(2) | Country code |
| batch_id | bigint | Load batch |
| source_system | varchar | Ingestion source |
| priority | int | Priority 1-5 |
| created_by | varchar | User or service that created the row |
| external_ref | varchar | Reference in upstream system |
