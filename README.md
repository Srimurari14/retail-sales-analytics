# Retail Sales Analytics – Data Engineering Pipeline

## Overview

This project implements an end-to-end data engineering pipeline using real e-commerce transactional data.
The pipeline ingests raw CSV files, performs joins, validation, cleaning, and transformations, and produces a curated dataset for analytics.

The pipeline is:

* Modular and reproducible
* Executed using Docker
* Orchestrated using Apache Airflow

The goal of this project is to demonstrate production-style data engineering practices, not just data analysis.

---

## Dataset

**Source:** Brazilian E-Commerce Public Dataset by Olist (Kaggle)
Link: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

**Description:**
The dataset contains approximately 100,000 orders placed between 2016 and 2018. It includes information about:

* Orders and order items
* Customers and sellers
* Payments
* Products and categories
* Geographic details

The data is anonymized and represents real commercial transactions.

---

## Architecture

### High-level flow

```
Raw CSV files
   ↓
Processing and joins
   ↓
Data cleaning and validation
   ↓
Feature transformations
   ↓
Curated dataset (final.csv)
```

### Execution model

* Python scripts implement pipeline logic
* Docker packages and runs the pipeline
* Apache Airflow schedules and orchestrates Docker runs

---

## Tools and Technologies

### Data Processing

* Python 3.11
* Pandas
* NumPy

### Containerization

* Docker
* Docker volumes for data persistence

### Orchestration

* Apache Airflow 2.9
* Docker Compose
* PostgreSQL (Airflow metadata database)

---

## Project Structure

```
retail-sales-analytics/
├── data/
│   ├── raw/            # Original CSV files
│   ├── processed/      # Joined intermediate datasets
│   ├── cleaned/        # Cleaned datasets
│   └── transformed/    # Final curated output
│
├── scripts/
│   ├── orders_with_items.py
│   ├── ord_itm_cust.py
│   ├── ord_pay.py
│   ├── ord_pay_prod.py
│   ├── ord_prod_sell.py
│   ├── clean.py
│   ├── transform.py
│   └── run_pipeline.py
│
├── airflow/
│   ├── dags/
│   │   └── retail_sales_pipeline_dag.py
│   ├── logs/
│   └── docker-compose.yml
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Pipeline Stages

### 1. Ingestion

* Reads raw CSV files from `data/raw`
* No filtering or assumptions applied at this stage

### 2. Processing

* Orders joined with items, customers, payments, products, and sellers
* One-to-many relationships preserved at order-item level
* Intermediate datasets written to `data/processed`

### 3. Cleaning

* Datetime normalization
* City name standardization (case, accents, spacing)
* Explicit data quality flags added:

  * `is_delivered`
  * `has_del_date`
  * `has_prod_dim`
  * `has_pay_info`

### 4. Transformation

* Item-level total value calculation
* Delivery duration calculation
* Payment method feature extraction
* Product volume calculation
* Monetary values rounded for consistency

### 5. Output

* Final curated dataset written to:

  ```
  data/transformed/final.csv
  ```

---

## Data Quality Notes

* Some delivered orders do not have delivery dates
* A small number of orders have no payment records
* Product dimension data is missing for a subset of products
* No rows are dropped silently
* Missing information is explicitly flagged

This approach ensures transparency and avoids data loss.

---

## Running the Pipeline with Docker

### Build the Docker image

Run from the project root:

```bash
docker build -t retail-sales-pipeline .
```

### Execute the pipeline

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  retail-sales-pipeline
```

This runs the full pipeline and generates `final.csv`.

---

## Running the Pipeline with Airflow

### Start Airflow

```bash
cd airflow
docker compose up -d
```

Access the Airflow UI:

```
http://localhost:8080
```

### Trigger the pipeline

* Enable the `retail_sales_pipeline` DAG
* Trigger it manually from the UI
* Monitor logs from the task view

The DAG runs the Dockerized pipeline end-to-end.

---

## Why Airflow Is Used

Docker is used to package and execute the pipeline logic.
Apache Airflow is used to:

* Schedule recurring runs
* Track execution history
* Handle retries and failures
* Orchestrate pipeline execution over time

Docker handles execution.
Airflow handles operations.

---

## Key Takeaways

* Built a modular data pipeline with clear stage separation
* Handled real-world data quality issues explicitly
* Packaged execution using Docker for reproducibility
* Orchestrated pipeline runs using Apache Airflow
* Followed production-aligned data engineering practices
