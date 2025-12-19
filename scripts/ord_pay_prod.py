import pandas as pd

ord_pay_simp = pd.read_csv('data/processed/ord_pay_simplified.csv')
products = pd.read_csv("data/raw/olist_products_dataset.csv")

products = products[['product_id', 'product_category_name', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']]

ord_pay_prod = pd.merge(ord_pay_simp, products, on='product_id', how='left')

ord_pay_prod.to_csv('data/processed/ord_pay_prod.csv', index=False)