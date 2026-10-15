---
title: OTD - operations definition
topic: on-time-delivery
updated: 2025-06-09
owner: finance
---

# OTD - operations definition

Owner: finance analytics.

`on_time = delivered_at <= promised_window_end + 30 minutes grace`

We now compare against the promised_window_end timestamp with a 30 minute grace period.
