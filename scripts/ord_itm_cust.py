import pandas as pd

orders_with_items = pd.read_csv("data/processed/orders_with_items.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")

orders_items_customers = pd.merge(orders_with_items, customers, on='customer_id', how='left')

orders_items_customers.to_csv('data/processed/ord_itm_cust.csv', index=False)