# Table subscriptions_staging

Status: INTERNAL | source: schemas/subscriptions_staging.md | updated: 2024-11-05
Evidence: internal per decisions/adr-019-subscriptions-v3.md

# Table subscriptions_staging

Intermediate staging table loaded hourly by the ingestion job. Not for reporting.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| batch_id | bigint | Load batch |
| notes | text | Free text notes |
| net_amount | decimal | Amount before tax |
| is_test | boolean | Test row flag |
| status | varchar | Lifecycle status |
| currency | char(3) | ISO currency |
| source_system | varchar | Ingestion source |
| pincode | varchar | Postal code |
| country | char(2) | Country code |
| city | varchar | City name |
| priority | int | Priority 1-5 |
| tax_amount | decimal | Tax amount |
