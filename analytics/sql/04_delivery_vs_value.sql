-- Impact of delivery speed on order value

WITH delivery_bucket AS (
  SELECT
    order_id,
    CASE
      WHEN delivery_days <= 3 THEN '0-3 days'
      WHEN delivery_days <= 7 THEN '4-7 days'
      ELSE '8+ days'
    END AS delivery_bucket,
    item_total_value
  FROM fact_sales
  WHERE is_delivered = true
    AND has_del_date = true
)
SELECT
  delivery_bucket,
  COUNT(DISTINCT order_id) AS orders,
  ROUND(AVG(item_total_value), 2) AS avg_item_value
FROM delivery_bucket
GROUP BY delivery_bucket
ORDER BY delivery_bucket;
