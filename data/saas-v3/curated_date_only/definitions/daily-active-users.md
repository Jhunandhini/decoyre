# How we count daily active users

Status: CURRENT | source: wiki/how-we-count-daily-active-users.md | updated: 2025-11-16
Evidence: latest dated document in topic

# How we count daily active users

This page explains how we calculate daily active users (DAU) at Nilgiri Cloud.

## Formula

`DAU = distinct users with any api_call in the day`

A user is active on a day if they made any API call.

## Where it is used

Weekly business review and the leadership dashboard.

## Changelog

- 2025-11-16: fixed a typo in the heading.

## Additional rules found in other documents

- From this quarter on, everyone should follow the finance team's page "DAU - product analytics definition". Please ignore the 2023 analytics write-up "How we count daily active users" when building reports. (from decisions/adr-013-daily-active-users.md)

## History (do not use)

- wiki/finance/dau-product-analytics-definition.md is STALE, superseded by wiki/how-we-count-daily-active-users.md
