import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")

st.title("Clothing Selection")

# 读取衣服数据
items = pd.read_excel("items.xlsx")

# 搜索
search = st.text_input("Search clothing")

if search:
    items = items[items["Name"].str.contains(search, case=False)]

# 侧边栏筛选
st.sidebar.header("Filters")

brand = st.sidebar.multiselect(
    "Brand",
    items["Brand"].unique()
)

color = st.sidebar.multiselect(
    "Color",
    items["Color"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    items["Category"].unique()
)

filtered = items.copy()

if brand:
    filtered = filtered[filtered["Brand"].isin(brand)]

if color:
    filtered = filtered[filtered["Color"].isin(color)]

if category:
    filtered = filtered[filtered["Category"].isin(category)]

st.write(f"{len(filtered)} items found")

# 商品展示（4列）
cols = st.columns(4)

for i, row in filtered.iterrows():

    col = cols[i % 4]

    with col:

        image = Image.open(row["ImagePath"])

        st.image(image, use_container_width=True)

        st.markdown(f"**{row['Name']}**")

        st.write(row["Brand"])

        st.write(row["Color"])

        if st.button("Add to Cart", key=row["ItemID"]):
            st.success("Added")
