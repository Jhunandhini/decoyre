# Table orders_staging

Status: INTERNAL | source: schemas/orders_staging.md | updated: 2024-11-05
Evidence: internal per decisions/adr-023-orders-v2.md

# Table orders_staging

Intermediate staging table loaded hourly by the ingestion job. Not for reporting.

## Columns

| column | type | description |
|---|---|---|
| id | bigint | Primary key |
| city | varchar | City name |
| updated_at | timestamp | Last update time |
| created_at | timestamp | Row creation time |
| gross_amount | decimal | Amount after tax |
| currency | char(3) | ISO currency |
| status | varchar | Lifecycle status |
| source_system | varchar | Ingestion source |
| partner_id | int | Partner FK |
| store_id | int | FK to stores |
| country | char(2) | Country code |
| pincode | varchar | Postal code |
| version | int | Row version |
