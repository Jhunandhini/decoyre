---
title: How we calculate average order value
topic: average-order-value
updated: 2025-12-12
owner: analytics
---

> Note: this page is deprecated, see wiki/finance/aov-analytics-definition.md.

# How we calculate average order value

This page explains how we calculate average order value (AOV) at Kovai Mart.

## Formula

`AOV = SUM(gross_amount) / COUNT(session_id)`

Average order value divides gross sales by the number of shopping sessions.

## Where it is used

Weekly business review and the leadership dashboard.

## Changelog

- 2025-12-12: fixed a typo in the heading.
