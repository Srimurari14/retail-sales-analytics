-- Revenue contribution by product category

SELECT
  product_category_name,
  SUM(item_total_value) AS total_revenue,
  COUNT(DISTINCT order_id) AS orders,
  ROUND(
    SUM(item_total_value)
    / SUM(SUM(item_total_value)) OVER (),
    4
  ) AS revenue_share
FROM fact_sales
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name
ORDER BY total_revenue DESC;
