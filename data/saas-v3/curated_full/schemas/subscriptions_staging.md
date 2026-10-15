# Table subscriptions_staging

Status: INTERNAL | source: schemas/subscriptions_staging.md | updated: 2024-11-05
Evidence: internal per decisions/adr-017-subscriptions-v3.md

# Table subscriptions_staging

Intermediate staging table loaded hourly by the ingestion job. Not for reporting.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| priority | int | Priority 1-5 |
| notes | text | Free text notes |
| city | varchar | City name |
| region_code | varchar | Region |
| currency | char(3) | ISO currency |
| gross_amount | decimal | Amount after tax |
| created_at | timestamp | Row creation time |
| external_ref | varchar | Reference in upstream system |
| is_test | boolean | Test row flag |
| created_by | varchar | User or service that created the row |
| version | int | Row version |
| updated_at | timestamp | Last update time |
