# Data Dictionary – Retail Sales Analytics (Olist)

## Overview

This project uses the **Brazilian E-Commerce Public Dataset by Olist**, which contains anonymized transactional data from multiple marketplaces between **2016–2018**.

The pipeline follows a layered approach:

* `raw` → original source files
* `processed` → structurally joined data
* `cleaned` → standardized and flagged data
* `transformed` → analytics-ready data

This document describes:

* the raw source tables
* the final transformed dataset
* key characteristics such as row counts, columns, and missing values

---

## Raw Source Tables

### 1. Orders (`olist_orders_dataset.csv`)

**Description**
Contains order-level information such as status, timestamps, and customer linkage.

**Grain**
One row per order.

**Key Columns**

* `order_id`
* `customer_id`
* `order_status`
* `order_purchase_timestamp`
* `order_delivered_customer_date`

**Notes**

* Not all orders are delivered
* Some delivered orders are missing delivery timestamps (known data quality gaps)
* Orders can exist without associated order items

---

### 2. Order Items (`olist_order_items_dataset.csv`)

**Description**
Contains item-level information for each order.

**Grain**
One row per order item.

**Key Columns**

* `order_id`
* `order_item_id`
* `product_id`
* `seller_id`
* `price`
* `freight_value`
* `shipping_limit_date`

**Notes**

* Orders can contain multiple items
* `price` and `freight_value` are **item-level metrics**
* No null values in core item attributes

---

### 3. Customers (`olist_customers_dataset.csv`)

**Description**
Contains customer location and identifier information.

**Grain**
One row per customer record.

**Key Columns**

* `customer_id`
* `customer_unique_id`
* `customer_city`
* `customer_state`
* `customer_zip_code_prefix`

**Notes**

* A single `customer_unique_id` can map to multiple `customer_id`s
* Customer location data is clean and complete

---

### 4. Payments (`olist_order_payments_dataset.csv`)

**Description**
Contains payment events associated with orders.

**Grain**
One row per payment event per order.

**Key Columns**

* `order_id`
* `payment_sequential`
* `payment_type`
* `payment_installments`
* `payment_value`

**Notes**

* Orders can have multiple payment records
* Multiple payment types can be used for a single order
* `payment_value` represents **order-level payment amounts**
* One known order exists without payment records

---

### 5. Products (`olist_products_dataset.csv`)

**Description**
Contains product metadata and physical dimensions.

**Grain**
One row per product.

**Key Columns**

* `product_id`
* `product_category_name`
* `product_weight_g`
* `product_length_cm`
* `product_height_cm`
* `product_width_cm`

**Notes**

* Some products lack category or dimension metadata
* Missing dimensions represent incomplete seller input, not errors

---

### 6. Sellers (`olist_sellers_dataset.csv`)

**Description**
Contains seller location information.

**Grain**
One row per seller.

**Key Columns**

* `seller_id`
* `seller_city`
* `seller_state`
* `seller_zip_code_prefix`

**Notes**

* Seller data is complete
* All seller IDs in transactional data exist in this table

---

## Final Transformed Dataset

### Final Fact Table (`final.csv`)

**Description**
A denormalized, item-level fact table enriched with order, customer, seller, product, and payment context.
This table is intended for analytics, dashboards, and downstream modeling.

**Grain**
One row per **order item**.

**Row Count**

* 113,425 rows

---

### Column Groups

#### Identifiers

* `order_id`
* `order_item_id`
* `product_id`
* `seller_id`
* `customer_id`
* `customer_unique_id`

---

#### Order & Delivery

* `order_status`
* `order_purchase_timestamp`
* `order_delivered_customer_date`
* `is_delivered`
* `has_del_date`

**Notes**

* Some delivered orders lack delivery timestamps (8 known cases)
* Delivery flags are used instead of imputing missing dates

---

#### Item & Product

* `price`
* `freight_value`
* `item_total_value`
* `product_category_name`
* `product_weight_g`
* `product_length_cm`
* `product_height_cm`
* `product_width_cm`
* `has_prod_dim`

**Notes**

* `item_total_value = price + freight_value`
* Product dimensions may be missing for a small number of items

---

#### Payments

* `payment_value`
* `payment_sequential`
* `payment_type`
* `payment_installments`
* `has_pay_info`
* `paid`

**Important**

* `payment_value` is an **order-level metric** and is repeated across item rows
* It must be aggregated at the order level to avoid double counting
* Payment types may include multiple instruments (e.g., credit card + voucher)

---

#### Location

* `customer_city`
* `customer_city_clean`
* `customer_state`
* `seller_city`
* `seller_city_clean`
* `seller_state`
* `customer_zip_code_prefix`
* `seller_zip_code_prefix`

**Notes**

* Cleaned city columns normalize casing, whitespace, and accents
* Original city columns are preserved for traceability

---

### Missing Values Summary

Missing values in the final dataset represent **real business conditions**, not processing errors:

* Orders without payment records (1 order, 3 items)
* Delivered orders missing delivery timestamps (8 orders)
* Products missing dimension metadata (18 items)
* Products without category classification

No missing values were imputed or removed.

---

## Design Notes

* Item-level and order-level metrics are intentionally co-located
* Boolean flags are used instead of modifying raw values
* The dataset preserves real-world inconsistencies to maintain analytical integrity
* Downstream consumers are expected to aggregate metrics at the correct grain