---
title: ADR-019: monthly MRR report source
updated: 2025-01-25
owner: data-council
---

# ADR-019: monthly MRR report source

Status: Accepted

## Decision

The monthly MRR report now reads from `subscriptions_v3`. `subscriptions_legacy_stripe` is deprecated and must no longer be used. `subscriptions_staging` is internal to ingestion.
