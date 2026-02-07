-- Delivery duration analysis for delivered orders

SELECT
  ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
  ROUND(
    COUNT(*) FILTER (WHERE delivery_days <= 7)::FLOAT
    / COUNT(*),
    4
  ) AS on_time_delivery_rate
FROM fact_sales
WHERE is_delivered = true
  AND has_del_date = true;
