-- Repeat customer analysis

WITH customer_orders AS (
  SELECT
    customer_unique_id,
    COUNT(DISTINCT order_id) AS orders
  FROM fact_sales
  GROUP BY customer_unique_id
)
SELECT
  COUNT(*) FILTER (WHERE orders > 1)::FLOAT
  / COUNT(*) AS repeat_customer_rate
FROM customer_orders;
