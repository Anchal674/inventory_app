import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Inventory Optimization Dashboard", layout="wide")
st.title("📦 Inventory Optimization & Sales Analysis")

# ================= Data Loading =================
@st.cache_data
def load_data():
    # Correct file paths
    sales = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Desktop\inventory_app\data\SalesFINAL12312016.csv")
    purchases = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Desktop\inventory_app\data\PurchasesFINAL12312016.csv")
    beg_inv = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Desktop\inventory_app\data\BegInvFINAL12312016.csv")
    end_inv = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Desktop\inventory_app\data\EndInvFINAL12312016.csv")
    return sales, purchases, beg_inv, end_inv

try:
    sales, purchases, beg_inv, end_inv = load_data()

    # ================= KPIs =================
    st.subheader("📊 Key Inventory KPIs")
    total_sales_qty = sales["SalesQuantity"].sum()
    total_purchase_qty = purchases["Quantity"].sum()
    avg_inventory = (beg_inv["onHand"].sum() + end_inv["onHand"].sum()) / 2

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales Quantity", f"{total_sales_qty:,.0f}")
    col2.metric("Total Purchase Quantity", f"{total_purchase_qty:,.0f}")
    col3.metric("Average Inventory", f"{avg_inventory:,.0f}")

    # ================= Sales Trend =================
    st.subheader("📈 Sales Trend")
    sales["SalesDate"] = pd.to_datetime(sales["SalesDate"])
    sales_trend = sales.groupby("SalesDate")["SalesQuantity"].sum()

    fig, ax = plt.subplots()
    sales_trend.plot(ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Quantity Sold")
    st.pyplot(fig)

    # ================= Inventory Turnover =================
    st.subheader("🔄 Inventory Turnover Ratio")
    inventory_turnover = total_sales_qty / avg_inventory
    st.metric("Inventory Turnover", round(inventory_turnover, 2))

    # ================= ABC Analysis =================
    st.subheader("🅰️ ABC Analysis")
    sales["SalesValue"] = sales["SalesQuantity"] * sales["SalesPrice"]
    abc = sales.groupby("Description")["SalesValue"].sum().sort_values(ascending=False)
    abc_cum = abc.cumsum() / abc.sum()

    abc_df = pd.DataFrame({
        "SalesValue": abc,
        "Cumulative %": abc_cum
    })

    def abc_category(x):
        if x <= 0.7:
            return "A"
        elif x <= 0.9:
            return "B"
        else:
            return "C"

    abc_df["Category"] = abc_df["Cumulative %"].apply(abc_category)
    st.dataframe(abc_df.head(20))

    # ================= Vendor Performance =================
    st.subheader("🚚 Vendor Performance")
    vendor_perf = purchases.groupby("VendorName")["Quantity"].sum().sort_values(ascending=False)
    st.bar_chart(vendor_perf.head(10))

except FileNotFoundError:
    st.error("❌ Data files not found. Please check the file paths in the script.")
