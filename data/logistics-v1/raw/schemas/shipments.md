---
title: Table shipments
topic: shipments-tables
updated: 2024-11-05
owner: data-eng
---

# Table shipments

Original shipments table from 2021. Raw rows, no cleaning.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| city | varchar | City name |
| net_amount | decimal | Amount before tax |
| status | varchar | Lifecycle status |
| created_by | varchar | User or service that created the row |
| tags | jsonb | Arbitrary tags |
| store_id | int | FK to stores |
| pincode | varchar | Postal code |
| gross_amount | decimal | Amount after tax |
| country | char(2) | Country code |
| partner_id | int | Partner FK |
