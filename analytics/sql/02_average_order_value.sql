-- Average Order Value computed at order grain

WITH order_totals AS (
  SELECT
    order_id,
    SUM(item_total_value) AS order_value
  FROM fact_sales
  GROUP BY order_id
)
SELECT
  ROUND(AVG(order_value), 2) AS avg_order_value
FROM order_totals;
