Title: Retail Sales Analytics

Problem Statement:
Businesses generate raw transactional sales data every day, but this data is often messy, inconsistent, and not immediately usable for analytics.
This project builds an end-to-end data engineering pipeline that ingests raw retail sales data, validates and cleans it, applies business transformations, stores it in structured layers (raw, clean, curated), and enables analytics through SQL queries.
The final output supports insights such as daily revenue trends, top-selling products, and customer purchase behavior.

Data:
Retail sales data with orders, customers, products, dates, prices/quantities

The raw and processed data files are not tracked in Git.

To reproduce the datasets:
1. Download the Olist Brazilian E-Commerce dataset from Kaggle  
2. Place the CSV files under `data/raw/`  
3. Run the processing scripts in the `scripts/` directory  

Pipeline Architecture:
Raw CSV files -> Ingestion -> Validation -> Cleaning -> Transformation ->Curated tables -> SQL analytics -> Dashboard  

KPIs:
Daily/ Monthly revenue  
Orders  
Average order value  
Unique customers  
