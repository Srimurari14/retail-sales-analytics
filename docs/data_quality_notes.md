# Data Quality Notes

## Purpose

This document outlines **known data quality characteristics, edge cases, and limitations** observed in the dataset during ingestion, processing, and transformation.
These issues are **intentional to preserve business truth** and were **not corrected or imputed** unless explicitly stated.

---

## General Principles

* No rows were dropped due to data quality issues
* No missing values were filled or imputed
* Boolean flags were added to explicitly surface data conditions
* All issues documented below reflect **real-world operational gaps**, not processing errors

---

## Known Data Quality Observations

### 1. Delivered Orders Without Delivery Timestamp

**Description**
There are **8 orders** where:

* `order_status = 'delivered'`
* `order_delivered_customer_date` is missing

**Impact**

* Delivery duration cannot be computed for these orders
* These rows are flagged using:

  * `is_delivered = True`
  * `has_del_date = False`
  * `delivery_completed = False`

**Handling**

* Values were left as null
* No delivery dates were inferred or backfilled

---

### 2. Orders Without Payment Records

**Description**
There is **1 order** in the orders dataset that does not appear in the payments dataset.
This order contains **3 items**, resulting in **3 rows** with missing payment information.

**Impact**

* `payment_value`, `payment_type`, and related fields are null for these rows
* Financial analysis at the order level should account for this edge case

**Handling**

* Rows were preserved
* Flag added:

  * `has_pay_info = False`

---

### 3. Order-Level Payment Value Repeated at Item Level

**Description**
`payment_value` represents the **total amount paid for an entire order**.
After joining to item-level data, this value is **repeated across all items of the order**.

**Impact**

* Summing `payment_value` across rows will result in over-counting
* This is expected and intentional

**Handling**

* Value was not redistributed across items
* Users must aggregate `payment_value` at the `order_id` level only

---

### 4. Products Missing Dimension Metadata

**Description**
There are **18 item rows** where one or more product dimension fields are missing:

* `product_weight_g`
* `product_length_cm`
* `product_height_cm`
* `product_width_cm`

**Impact**

* Volume or logistics-related calculations cannot be performed for these rows

**Handling**

* No imputation was performed
* Flag added:

  * `has_prod_dim = False`

---

### 5. Products Without Category Classification

**Description**
Some products lack a `product_category_name`.

**Impact**

* Category-based aggregations will exclude these products unless handled explicitly

**Handling**

* Missing categories were preserved
* Category translation and enrichment are deferred to a later stage

---

### 6. City Name Representation Variability

**Description**
City names contain representational inconsistencies:

* casing differences
* accents and diacritics
* extra whitespace

Examples:

* `São Paulo`, `sao paulo`, `SÃO PAULO`

**Impact**

* Grouping by raw city names can result in duplicate buckets

**Handling**

* Cleaned city columns were added:

  * `customer_city_clean`
  * `seller_city_clean`
* Cleaning included:

  * trimming whitespace
  * lowercasing
  * removing diacritics
* Original city columns were preserved

---

### 7. Orders Without Items

**Description**
Some orders exist in the orders table but have no associated order items.

**Impact**

* Item-level attributes (`product_id`, `seller_id`, `price`) are null for these rows

**Handling**

* Rows were preserved to maintain referential completeness
* No assumptions were made about missing items

---

## Summary

All data quality issues observed in this project:

* are limited in scope
* are explicitly documented
* reflect real operational behavior
* are surfaced using flags rather than corrected silently

Downstream consumers are expected to:

* aggregate metrics at the correct grain
* use provided flags to filter or segment data as needed
