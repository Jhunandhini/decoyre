# Delivery SLA

Status: current

- Orders in city zones must be delivered within 2 hours.
- For rural pincodes the delivery SLA is 24 hours instead of the city target.
- The delivery SLA clock starts at payment_confirmed_at, not at order creation.
- Public holidays are excluded from the delivery SLA calculation.
