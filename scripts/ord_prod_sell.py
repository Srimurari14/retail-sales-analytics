import pandas as pd

ord_pay_prod = pd.read_csv('data/processed/ord_pay_prod.csv')
sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")

ord_prod_sell = pd.merge(ord_pay_prod, sellers, on='seller_id', how='left')

ord_prod_sell.to_csv('data/processed/ord_prod_sell.csv', index=False)