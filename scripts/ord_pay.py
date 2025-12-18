import pandas as pd

ord_itm_cust = pd.read_csv('data/processed/ord_itm_cust.csv')
payments = pd.read_csv('data/raw/olist_order_payments_dataset.csv')

ptm = payments.groupby('order_id').agg({'payment_sequential':'max', 'payment_type':list, 'payment_installments':'max', 'payment_value':'sum'}).reset_index()


ord_pay = pd.merge(ord_itm_cust, payments, on='order_id', how='left')

ord_pay_simp = pd.merge(ord_itm_cust, ptm, on='order_id', how='left')

ptm.to_csv('data/processed/pay_simplified.csv', index=False)
ord_pay.to_csv('data/processed/ord_pay.csv', index=False)
ord_pay_simp.to_csv('data/processed/ord_pay_simplified.csv', index=False)
