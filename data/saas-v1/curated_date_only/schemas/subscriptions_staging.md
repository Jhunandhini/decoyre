# Table subscriptions_staging

Status: STALE | source: schemas/subscriptions_staging.md | updated: 2024-11-05
Evidence: older than schemas/subscriptions_v3.md

# Table subscriptions_staging

Intermediate staging table loaded hourly by the ingestion job. Not for reporting.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| source_system | varchar | Ingestion source |
| updated_at | timestamp | Last update time |
| pincode | varchar | Postal code |
| gross_amount | decimal | Amount after tax |
| is_test | boolean | Test row flag |
| tax_amount | decimal | Tax amount |
| net_amount | decimal | Amount before tax |
| customer_id | bigint | FK to customers |
| status | varchar | Lifecycle status |
| tags | jsonb | Arbitrary tags |
| partner_id | int | Partner FK |
| notes | text | Free text notes |
