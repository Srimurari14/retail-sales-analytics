import unicodedata
import pandas as pd

data = pd.read_csv("data/processed/ord_prod_sell.csv")

data["is_delivered"] = data["order_status"] == "delivered"
data["has_del_date"] = data["order_delivered_customer_date"].notna()
data["has_prod_dim"] = data["product_weight_g"].notna()
data["has_pay_info"] = data["payment_value"].notna()

data["order_purchase_timestamp"] = pd.to_datetime(data["order_purchase_timestamp"])
data["order_delivered_customer_date"] = pd.to_datetime(data["order_delivered_customer_date"])
data["shipping_limit_date"] = pd.to_datetime(data["shipping_limit_date"])

data["customer_city_clean"] = (
    data["customer_city"]
        .str.strip()
        .str.lower()
        .apply(
            lambda x: unicodedata.normalize("NFKD", x)
            .encode("ascii", "ignore")
            .decode("utf-8") if pd.notna(x) else x
        )
)

data["seller_city_clean"] = (
    data["seller_city"]
        .str.strip()
        .str.lower()
        .apply(
            lambda x: unicodedata.normalize("NFKD", x)
            .encode("ascii", "ignore")
            .decode("utf-8") if pd.notna(x) else x
        )
)

data.to_csv("data/cleaned/cleaned.csv", index=False)
