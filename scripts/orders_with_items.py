import pandas as pd

orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")

orders = orders[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 'order_delivered_customer_date']]

orders_with_items = pd.merge(orders, order_items, on='order_id', how='left')

orders_with_items.to_csv('data/processed/orders_with_items.csv', index=False)