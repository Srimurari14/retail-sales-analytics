import ast
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transformed" / "final.csv"

st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="📈",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"], errors="coerce"
    )

    # Normalize payment_type list strings into real lists
    def parse_payment_list(value: str) -> list[str]:
        try:
            parsed = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return ["unknown"]
        if isinstance(parsed, list):
            return [str(v) for v in parsed if v]
        return [str(parsed)] if parsed else ["unknown"]

    df["payment_type_list"] = df["payment_type"].fillna("[]").map(parse_payment_list)
    df["primary_payment_type"] = df["payment_type_list"].map(
        lambda values: values[0] if values else "unknown"
    )
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    return df


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def metric_row(df: pd.DataFrame) -> None:
    total_revenue = df["item_total_value"].sum()
    total_orders = df["order_id"].nunique()
    aov = total_revenue / total_orders if total_orders else 0
    avg_delivery = df.loc[df["is_delivered"].astype(bool), "delivery_days"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", format_currency(total_revenue))
    col2.metric("Orders", f"{total_orders:,.0f}")
    col3.metric("Average Order Value", f"${aov:,.2f}")
    col4.metric("Avg Delivery Days", f"{avg_delivery:,.1f}" if pd.notna(avg_delivery) else "—")


def filtered_data(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")

    min_date = df["order_purchase_timestamp"].min()
    max_date = df["order_purchase_timestamp"].max()
    date_range = st.sidebar.date_input(
        "Purchase Date",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
    )

    selected_states = st.sidebar.multiselect(
        "Customer State",
        options=sorted(df["customer_state"].dropna().unique()),
        default=None,
    )

    selected_categories = st.sidebar.multiselect(
        "Product Category",
        options=sorted(df["product_category_name"].dropna().unique()),
        default=None,
    )

    selected_payment = st.sidebar.multiselect(
        "Primary Payment Type",
        options=sorted(df["primary_payment_type"].dropna().unique()),
        default=None,
    )

    voucher_only = st.sidebar.radio(
        "Voucher Usage",
        options=["All", "Voucher Used", "No Voucher"],
        index=0,
    )

    filtered = df.copy()
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[
        (filtered["order_purchase_timestamp"] >= start)
        & (filtered["order_purchase_timestamp"] <= end)
    ]

    if selected_states:
        filtered = filtered[filtered["customer_state"].isin(selected_states)]
    if selected_categories:
        filtered = filtered[filtered["product_category_name"].isin(selected_categories)]
    if selected_payment:
        filtered = filtered[filtered["primary_payment_type"].isin(selected_payment)]
    if voucher_only == "Voucher Used":
        filtered = filtered[filtered["used_voucher"] == True]
    elif voucher_only == "No Voucher":
        filtered = filtered[filtered["used_voucher"] == False]

    return filtered


def chart_revenue_by_category(df: pd.DataFrame) -> None:
    grouped = (
        df.groupby("product_category_name", dropna=False)["item_total_value"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )
    fig = px.bar(
        grouped,
        x="item_total_value",
        y="product_category_name",
        orientation="h",
        title="Top 15 Categories by Revenue",
        labels={"item_total_value": "Revenue", "product_category_name": "Category"},
    )
    fig.update_layout(height=420, yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig, use_container_width=True)


def chart_orders_over_time(df: pd.DataFrame) -> None:
    grouped = (
        df.groupby("order_month")["order_id"].nunique().reset_index(name="orders")
    )
    fig = px.line(
        grouped,
        x="order_month",
        y="orders",
        title="Orders Over Time",
        labels={"order_month": "Month", "orders": "Orders"},
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)


def chart_aov_over_time(df: pd.DataFrame) -> None:
    grouped = (
        df.groupby("order_month")["item_total_value"].sum().reset_index()
    )
    grouped["orders"] = df.groupby("order_month")["order_id"].nunique().values
    grouped["aov"] = grouped["item_total_value"] / grouped["orders"]
    fig = px.line(
        grouped,
        x="order_month",
        y="aov",
        title="Average Order Value Over Time",
        labels={"order_month": "Month", "aov": "AOV"},
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)


def chart_delivery_by_state(df: pd.DataFrame) -> None:
    delivered = df[df["is_delivered"].astype(bool)]
    grouped = (
        delivered.groupby("customer_state")["delivery_days"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = px.bar(
        grouped,
        x="customer_state",
        y="delivery_days",
        title="Average Delivery Days by State",
        labels={"customer_state": "State", "delivery_days": "Avg Delivery Days"},
    )
    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)


def chart_payment_mix(df: pd.DataFrame) -> None:
    exploded = df.explode("payment_type_list")
    grouped = (
        exploded.groupby("payment_type_list")["order_id"].nunique().reset_index(name="orders")
    )
    fig = px.pie(
        grouped,
        names="payment_type_list",
        values="orders",
        title="Payment Method Mix",
    )
    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)


def chart_voucher_impact(df: pd.DataFrame) -> None:
    grouped = (
        df.groupby("used_voucher")["item_total_value"].sum().reset_index()
    )
    grouped["orders"] = df.groupby("used_voucher")["order_id"].nunique().values
    grouped["aov"] = grouped["item_total_value"] / grouped["orders"]
    grouped["used_voucher"] = grouped["used_voucher"].map({True: "Voucher", False: "No Voucher"})
    fig = px.bar(
        grouped,
        x="used_voucher",
        y="aov",
        title="Voucher Impact on AOV",
        labels={"used_voucher": "Voucher Usage", "aov": "AOV"},
    )
    fig.update_layout(height=320)
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.title("Retail Sales Analytics Dashboard")
    st.caption("Interactive view of revenue, orders, delivery performance, and customer behavior.")

    if not DATA_PATH.exists():
        st.error(f"Data file not found: {DATA_PATH}")
        st.stop()

    df = load_data(DATA_PATH)
    filtered = filtered_data(df)

    metric_row(filtered)

    left, right = st.columns((1.1, 1))
    with left:
        chart_revenue_by_category(filtered)
    with right:
        chart_payment_mix(filtered)

    left, right = st.columns(2)
    with left:
        chart_orders_over_time(filtered)
    with right:
        chart_aov_over_time(filtered)

    left, right = st.columns(2)
    with left:
        chart_delivery_by_state(filtered)
    with right:
        chart_voucher_impact(filtered)

    st.divider()
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered.head(200), use_container_width=True)


if __name__ == "__main__":
    main()
