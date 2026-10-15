# Table shipments_legacy_tms

Status: STALE | source: schemas/shipments_legacy_tms.md | updated: 2024-11-05
Evidence: older than schemas/shipments_v2.md

# Table shipments_legacy_tms

This is the table we use for the monthly delivery report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| created_by | varchar | User or service that created the row |
| tax_amount | decimal | Tax amount |
| region_code | varchar | Region |
| priority | int | Priority 1-5 |
| deleted_at | timestamp | Soft delete time |
| tags | jsonb | Arbitrary tags |
| currency | char(3) | ISO currency |
| partner_id | int | Partner FK |
| updated_at | timestamp | Last update time |
| gross_amount | decimal | Amount after tax |
| store_id | int | FK to stores |
| customer_id | bigint | FK to customers |
| city | varchar | City name |
| notes | text | Free text notes |
| external_ref | varchar | Reference in upstream system |
| version | int | Row version |
| status | varchar | Lifecycle status |
| cash_due | decimal | Cash due |
| pincode | varchar | Postal code |
| created_at | timestamp | Row creation time |
| is_test | boolean | Test row flag |
| batch_id | bigint | Load batch |
| truck_type | varchar | Truck type |
| source_system | varchar | Ingestion source |
