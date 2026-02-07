-- Voucher usage vs order value (simple & robust)

WITH order_values AS (
  SELECT
    order_id,
    MAX(used_voucher) AS used_voucher,
    SUM(item_total_value) AS order_value
  FROM fact_sales
  WHERE has_pay_info = true
  GROUP BY order_id
)
SELECT
  used_voucher,
  COUNT(order_id) AS orders,
  ROUND(AVG(order_value), 2) AS avg_order_value
FROM order_values
GROUP BY used_voucher;