# On-time delivery rate

Status: current (since 2025-04-16, decisions/adr-016-on-time-delivery.md)

`on_time = delivered_at <= promised_window_end + 30 minutes grace`

We now compare against the promised_window_end timestamp with a 30 minute grace period.

The 2023 definition in wiki/how-we-calculate-on-time-delivery.md is deprecated.
