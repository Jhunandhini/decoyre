# Table shipments_legacy_tms

Status: DEPRECATED | source: schemas/shipments_legacy_tms.md | updated: 2024-11-05
Evidence: deprecated by decisions/adr-020-shipments-v2.md

# Table shipments_legacy_tms

This is the table we use for the monthly delivery report.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| version | int | Row version |
| city | varchar | City name |
| external_ref | varchar | Reference in upstream system |
| tax_amount | decimal | Tax amount |
| batch_id | bigint | Load batch |
| priority | int | Priority 1-5 |
| region_code | varchar | Region |
| status | varchar | Lifecycle status |
| partner_id | int | Partner FK |
| pincode | varchar | Postal code |
| currency | char(3) | ISO currency |
| store_id | int | FK to stores |
| gross_amount | decimal | Amount after tax |
| deleted_at | timestamp | Soft delete time |
| is_test | boolean | Test row flag |
| source_system | varchar | Ingestion source |
| net_amount | decimal | Amount before tax |
| updated_at | timestamp | Last update time |
| created_at | timestamp | Row creation time |
| notes | text | Free text notes |
| cash_due | decimal | Cash due |
| customer_id | bigint | FK to customers |
| tags | jsonb | Arbitrary tags |
| truck_type | varchar | Truck type |
