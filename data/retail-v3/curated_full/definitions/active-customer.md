# Active customer - CRM definition

Status: CURRENT | source: wiki/finance/active-customer-crm-definition.md | updated: 2025-03-19
Evidence: declared authoritative by decisions/adr-018-active-customer.md

# Active customer - CRM definition

Owner: finance analytics.

`active_customer = customer with at least one completed order in the trailing 60 days`

App sessions no longer count because bots and password resets inflated the number.

## History (do not use)

- wiki/how-we-count-active-customers.md is DEPRECATED, superseded by wiki/finance/active-customer-crm-definition.md
