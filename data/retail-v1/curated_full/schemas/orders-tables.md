# Orders Tables (which table to use)

Status of each table in this family:

- `orders`: STALE (not the declared current table) -> read [schemas/orders]
- `orders_legacy_pos`: DEPRECATED (deprecated by decisions/adr-019-orders-v2.md) -> read [schemas/orders_legacy_pos]
- `orders_staging`: INTERNAL (internal per decisions/adr-019-orders-v2.md) -> read [schemas/orders_staging]
- `orders_v2`: CURRENT (declared authoritative by decisions/adr-019-orders-v2.md) -> read [schemas/orders_v2]
