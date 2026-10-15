---
title: How we calculate on-time delivery
topic: on-time-delivery
updated: 2025-10-06
owner: analytics
---

# How we calculate on-time delivery

This page explains how we calculate on-time delivery rate at Palar Logistics.

## Formula

`on_time = delivered_at::date <= promised_date`

A shipment is on time if it was delivered on or before the promised_date.

## Where it is used

Weekly business review and the leadership dashboard.

## Changelog

- 2025-10-06: fixed a typo in the heading.
