# Table shipments_legacy_tms

Status: STALE | source: schemas/shipments_legacy_tms.md | updated: 2024-11-05
Evidence: older than schemas/shipments_v2.md

# Table shipments_legacy_tms

This is the table we use for the monthly delivery report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| tags | jsonb | Arbitrary tags |
| store_id | int | FK to stores |
| is_test | boolean | Test row flag |
| updated_at | timestamp | Last update time |
| city | varchar | City name |
| batch_id | bigint | Load batch |
| priority | int | Priority 1-5 |
| deleted_at | timestamp | Soft delete time |
| customer_id | bigint | FK to customers |
| created_by | varchar | User or service that created the row |
| notes | text | Free text notes |
| version | int | Row version |
| source_system | varchar | Ingestion source |
| status | varchar | Lifecycle status |
| country | char(2) | Country code |
| cash_due | decimal | Cash due |
| pincode | varchar | Postal code |
| created_at | timestamp | Row creation time |
| partner_id | int | Partner FK |
| tax_amount | decimal | Tax amount |
| currency | char(3) | ISO currency |
| truck_type | varchar | Truck type |
| gross_amount | decimal | Amount after tax |
| net_amount | decimal | Amount before tax |
