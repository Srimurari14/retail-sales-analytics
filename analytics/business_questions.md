# Business Questions

This section outlines the core business questions this analytics layer is designed to answer.
Questions are grouped by domain and are intentionally scoped to be answerable using the current dataset and analytics grain (order-item level).

## Revenue & Product Performance

1. Which product categories contribute the highest share of total revenue?
2. Is revenue concentrated among a small number of categories or products (Pareto effect)?
3. How does item price and freight cost contribute to total item value?
4. Are heavier or larger products associated with higher revenue or higher delivery times?

## Delivery & Logistics Performance

5. What is the average delivery time for delivered orders?
6. How does delivery duration vary by state and seller?
7. Are longer delivery times associated with lower order values?
8. What percentage of delivered orders meet a defined delivery SLA (e.g., ≤ 7 days)?

## Payment & Checkout Behavior

9. Which payment methods are most commonly used?
10. Are certain payment methods associated with higher order values?
11. Do orders using vouchers behave differently in terms of value or delivery time?
12. Does the number of payment methods used correlate with order value?

## Customer & Regional Trends

13. How does order value vary across customer states and cities?
14. Do repeat customers (same customer_unique_id) tend to place higher-value orders?
15. Are certain regions consistently associated with slower deliveries?

