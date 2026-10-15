---
title: ADR-019: monthly sales report source
updated: 2025-01-25
owner: data-council
---

# ADR-019: monthly sales report source

Status: Accepted

## Decision

The monthly sales report now reads from `orders_v2`. `orders_legacy_pos` is deprecated and must no longer be used. `orders_staging` is internal to ingestion.
