# MRR (monthly recurring revenue)

Status: CURRENT | source: wiki/mrr-monthly-recurring-revenue.md | updated: 2025-02-10
Evidence: latest dated document in topic

# MRR (monthly recurring revenue)

MRR is the sum of monthly_fee for all subscriptions with status active.

See related decisions for exceptions.

## Additional rules found in other documents

- Trial subscriptions are excluded from MRR even if they have a monthly_fee. (from decisions/adr-015-adr-on-mrr-and-trials.md)
- The monthly MRR report now reads from `subscriptions_v3`. `subscriptions_legacy_stripe` is deprecated and must no longer be used. `subscriptions_staging` is internal to ingestion. (from decisions/adr-017-subscriptions-v3.md)
- MRR in USD or EUR is converted to INR at the month-end exchange rate. (from finance/multi-currency-reporting.md)
- For MRR, annual plans are divided by 12 to get the monthly amount. (from notes/finance-sync-on-annual-plans.md)
- We moved to revenue churn: MRR lost from cancellations and downgrades over MRR at month start. (from wiki/finance/churn-revenue-churn-definition.md)
