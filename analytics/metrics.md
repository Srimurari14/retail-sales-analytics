# Metric Definitions

This document defines the core metrics used in the analytics layer.
All metrics are computed from the analytics fact table (`fact_sales`) at the order-item grain unless otherwise specified.

## Revenue Metrics

### Total Revenue
- **Definition:** Sum of `item_total_value`
- **Formula:** `SUM(item_total_value)`
- **Grain:** Order-item
- **Notes:** Includes item price and freight cost

### Average Order Value (AOV)
- **Definition:** Average revenue per order
- **Formula:** `SUM(item_total_value) / COUNT(DISTINCT order_id)`
- **Grain:** Order
- **Notes:** Aggregation must occur at the order level to avoid over-counting

### Revenue by Category
- **Definition:** Total revenue grouped by product category
- **Formula:** `SUM(item_total_value) GROUP BY product_category_name`
- **Grain:** Order-item

## Delivery Metrics

### Average Delivery Time
- **Definition:** Average number of days from purchase to delivery
- **Formula:** `AVG(delivery_days)`
- **Filter:** `is_delivered = true AND has_del_date = true`
- **Grain:** Order

### On-Time Delivery Rate
- **Definition:** Percentage of delivered orders completed within SLA
- **SLA:** ≤ 7 days
- **Formula:** `COUNT(delivery_days <= 7) / COUNT(is_delivered = true)`
- **Grain:** Order

## Payment Metrics

### Payment Method Mix
- **Definition:** Distribution of payment methods used
- **Formula:** `COUNT(*) GROUP BY payment_type`
- **Grain:** Order
- **Notes:** Payment attributes are order-level and repeated at item grain

### Voucher Usage Rate
- **Definition:** Percentage of orders using vouchers
- **Formula:** `COUNT(used_voucher = true) / COUNT(order_id)`
- **Grain:** Order

## Customer Metrics

### Orders per Customer
- **Definition:** Average number of orders per unique customer
- **Formula:** `COUNT(DISTINCT order_id) / COUNT(DISTINCT customer_unique_id)`
- **Grain:** Customer

### Repeat Customer Rate
- **Definition:** Percentage of customers with more than one order
- **Formula:** `COUNT(customers with >1 order) / COUNT(total customers)`
- **Grain:** Customer

## Data Quality Metrics

### Missing Delivery Date Rate
- **Definition:** Percentage of delivered orders without delivery timestamp
- **Formula:** `COUNT(has_del_date = false AND is_delivered = true) / COUNT(is_delivered = true)`

### Missing Payment Information Rate
- **Definition:** Percentage of orders without payment records
- **Formula:** `COUNT(has_pay_info = false) / COUNT(order_id)`

