# Table shipments_v2

Status: CURRENT | source: schemas/shipments_v2.md | updated: 2025-01-20
Evidence: declared authoritative by decisions/adr-026-shipments-v2.md

# Table shipments_v2

Cleaned shipments table, one row per shipment. Deduplicated.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| version | int | Row version |
| net_amount | decimal | Amount before tax |
| tax_amount | decimal | Tax amount |
| status | varchar | Lifecycle status |
| currency | char(3) | ISO currency |
| notes | text | Free text notes |
| batch_id | bigint | Load batch |
| created_by | varchar | User or service that created the row |
| tags | jsonb | Arbitrary tags |
| pincode | varchar | Postal code |
| source_system | varchar | Ingestion source |
| created_at | timestamp | Row creation time |
| partner_id | int | Partner FK |
| updated_at | timestamp | Last update time |
| deleted_at | timestamp | Soft delete time |
| city | varchar | City name |
| store_id | int | FK to stores |
| is_test | boolean | Test row flag |
| vehicle_class | varchar | Vehicle type: bike, van, 14ft truck |
| customer_id | bigint | FK to customers |
| country | char(2) | Country code |
| external_ref | varchar | Reference in upstream system |
| region_code | varchar | Region |
| cod_amount | decimal | Cash on delivery amount to collect |
