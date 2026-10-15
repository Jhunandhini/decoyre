---
title: Table subscriptions_legacy_stripe
topic: subscriptions-tables
updated: 2024-11-05
owner: data-eng
---

# Table subscriptions_legacy_stripe

This is the table we use for the monthly MRR report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| pincode | varchar | Postal code |
| country | char(2) | Country code |
| region_code | varchar | Region |
| created_at | timestamp | Row creation time |
| version | int | Row version |
| external_ref | varchar | Reference in upstream system |
| tax_amount | decimal | Tax amount |
| priority | int | Priority 1-5 |
| updated_at | timestamp | Last update time |
| status | varchar | Lifecycle status |
| deleted_at | timestamp | Soft delete time |
| created_by | varchar | User or service that created the row |
| is_test | boolean | Test row flag |
| city | varchar | City name |
| store_id | int | FK to stores |
| gross_amount | decimal | Amount after tax |
| partner_id | int | Partner FK |
| users_n | int | Number of users |
| batch_id | bigint | Load batch |
| notes | text | Free text notes |
| plan_period | varchar | Plan period |
| currency | char(3) | ISO currency |
| tags | jsonb | Arbitrary tags |
| customer_id | bigint | FK to customers |
