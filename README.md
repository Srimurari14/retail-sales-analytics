# Retail Sales Analytics (Data Engineering Project)

## Summary
This project builds a full data engineering pipeline on real e‑commerce data and produces an analytics‑ready dataset. The output is used for SQL analysis and dashboards that answer business questions about revenue, delivery performance, and customer behavior.

## Data Source
Brazilian E‑Commerce Public Dataset by Olist (Kaggle): [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains about 100,000 orders from 2016–2018, including customers, sellers, payments, products, and delivery events.

## Project Flow
```
Raw CSV files
  -> Processing & joins
  -> Cleaning & validation
  -> Feature engineering
  -> Curated dataset (data/transformed/final.csv)
  -> SQL analysis and dashboards
```

## What The Pipeline Does
### 1. Ingestion
Reads raw CSVs from `data/raw` without filtering.

### 2. Processing
Joins orders with items, customers, payments, products, and sellers.
Keeps one‑to‑many relationships at the item level.
Writes intermediate outputs to `data/processed`.

### 3. Cleaning and Validation
Normalizes datetimes.
Standardizes city names.
Adds explicit data quality flags:
- `is_delivered`
- `has_del_date`
- `has_prod_dim`
- `has_pay_info`

### 4. Feature Engineering
Computes item‑level total value and delivery duration.
Extracts voucher usage and payment method counts.
Calculates product volume.

### 5. Output
Final dataset for analytics:
`data/transformed/final.csv`

## Data Quality Approach
- No silent row drops.
- No missing value imputation.
- Real gaps stay visible through explicit flags.

## Analytics Layer
SQL queries in `analytics/sql` answer:
- Revenue and order trends.
- Category revenue contribution.
- Delivery performance by state.
- Voucher impact on average order value.

Results are written to `analytics/results`.

## Dashboards
### Tableau
Dashboard screenshot: `dashboards/tableau_dashboard.png`
Tableau Public link: [https://public.tableau.com/app/profile/sri.murari.dachepalli/viz/E-CommerceSalesDeliveryPerformanceDashboard/Dashboard1](https://public.tableau.com/app/profile/sri.murari.dachepalli/viz/E-CommerceSalesDeliveryPerformanceDashboard/Dashboard1)

### Streamlit (Local)
```
pip install -r requirements.txt
streamlit run dashboards/streamlit_dashboard.py
```

## Project Structure
```
retail-sales-analytics/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── cleaned/
│   └── transformed/
├── scripts/
├── analytics/
│   ├── sql/
│   └── results/
├── airflow/
├── dashboards/
├── Dockerfile
├── requirements.txt
└── README.md
```

## How To Run
### Local (Python)
```
pip install -r requirements.txt
python scripts/run_pipeline.py
```

### Docker
```
docker build -t retail-sales-pipeline .
docker run --rm -v $(pwd)/data:/app/data retail-sales-pipeline
```

### Airflow
```
cd airflow
docker compose up -d
```
Open [http://localhost:8080](http://localhost:8080) and trigger `retail_sales_pipeline`.
