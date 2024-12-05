import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_popular_products_df(products_df):
    popular_products_df = products_df.groupby(by="product_id")
    return popular_products_df

def create_top_sellers_df(order_items_df):
    top_sellers_df = order_items_df.groupby(by="seller_id")
    return top_sellers_df

products_df = pd.read_csv("products_clean.csv")
order_items_df = pd.read_csv("order_items_clean.csv")
customers_df = pd.read_csv("customers_clean.csv")

datetime_columns = ["shipping_limit_date"]
order_items_df.sort_values(by="shipping_limit_date", inplace=True)
order_items_df.reset_index(inplace=True)

for column in datetime_columns:
    order_items_df[column] = pd.to_datetime(order_items_df[column])

min_date = order_items_df["shipping_limit_date"].min()
max_date = order_items_df["shipping_limit_date"].max()

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/0/05/Flag_of_Brazil.svg/1280px-Flag_of_Brazil.svg.png")
    
    start_date, end_date = st.date_input(
        label="Rentang Waktu",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = order_items_df[(order_items_df["shipping_limit_date"] >= str(start_date)) & 
                (order_items_df["shipping_limit_date"] <= str(end_date))]

popular_products_df = create_popular_products_df(main_df)
top_sellers_df = create_top_sellers_df(main_df)

st.header("E-Commerce in Brazil :sparkles:")

st.subheader("Top 10 Sellers")

top_sellers = order_items_df["seller_id"].value_counts().head(10)
top_sellers.plot(kind="bar", figsize=(10, 5), color="skyblue", title="Top 10 Penjual")
st.pyplot(plt)

st.subheader("Top 10 Kota dengan Pelanggan Terbanyak")

top_cities = customers_df["customer_city"].value_counts().head(10)

top_cities.plot(kind="bar", figsize=(10, 5), color="skyblue", title="Top 10 Kota dengan Pelanggan Terbanyak")
plt.xlabel("Kota")
plt.ylabel("Jumlah Pelanggan")
plt.xticks(rotation=45)
st.pyplot(plt)

st.subheader("Top 10 Negara Bagian dengan Pelanggan Terbanyak")

top_states = customers_df["customer_state"].value_counts().head(10)

top_states.plot(kind="bar", figsize=(10, 5), color="blue", title="Top 10 Negara Bagian dengan Pelanggan Terbanyak")
plt.xlabel("Negara Bagian")  
plt.ylabel("Jumlah Pelanggan")  
plt.xticks(rotation=45)
st.pyplot(plt)