---
title: ADR-020: monthly delivery report source
updated: 2025-01-25
owner: data-council
---

# ADR-020: monthly delivery report source

Status: Accepted

## Decision

The monthly delivery report now reads from `shipments_v2`. `shipments_legacy_tms` is deprecated and must no longer be used. `shipments_staging` is internal to ingestion.
