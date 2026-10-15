# Table shipments_v2 (current)

Authoritative shipments table; source of the monthly delivery report. Do not use shipments_legacy_tms (deprecated), shipments (deprecated) or shipments_staging (ingestion only).

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| external_ref | varchar | Reference in upstream system |
| version | int | Row version |
| tax_amount | decimal | Tax amount |
| pincode | varchar | Postal code |
| created_by | varchar | User or service that created the row |
| status | varchar | Lifecycle status |
| net_amount | decimal | Amount before tax |
| source_system | varchar | Ingestion source |
| customer_id | bigint | FK to customers |
| partner_id | int | Partner FK |
| store_id | int | FK to stores |
| gross_amount | decimal | Amount after tax |
| tags | jsonb | Arbitrary tags |
| country | char(2) | Country code |
| city | varchar | City name |
| priority | int | Priority 1-5 |
| notes | text | Free text notes |
| vehicle_class | varchar | Vehicle type: bike, van, 14ft truck |
| cod_amount | decimal | Cash on delivery amount to collect |
| batch_id | bigint | Load batch |
| region_code | varchar | Region |
| currency | char(3) | ISO currency |
| updated_at | timestamp | Last update time |
| is_test | boolean | Test row flag |
