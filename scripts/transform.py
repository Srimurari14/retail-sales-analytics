import ast
import pandas as pd

data = pd.read_csv('data/cleaned/cleaned.csv')

data.item_total_value = data.price + data.freight_value

data.price = round(data.price, 2)
data.item_total_value = round(data.item_total_value, 2)

data.delivery_days = (pd.to_datetime(data.order_delivered_customer_date)- pd.to_datetime(data.order_purchase_timestamp)).dt.days

data.payment_type = data.payment_type.apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
data.num_pay_methods =  data.payment_type.str.len()
data.used_voucher = data.payment_type.apply(lambda x: 'voucher' in x if isinstance(x, list) else False)

data.product_volume_cm3 = data.product_length_cm * data.product_height_cm * data.product_width_cm

data.to_csv('data/transformed/transformed.csv', index=False)