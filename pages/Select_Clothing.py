import streamlit as st
import pandas as pd
from PIL import Image

st.title("Clothing Selection")

# 读取衣服数据
items = pd.read_excel("items.xlsx")

# 侧边栏筛选
st.sidebar.header("Filter")

brand_filter = st.sidebar.multiselect(
    "Brand",
    items["Brand"].unique()
)

color_filter = st.sidebar.multiselect(
    "Color",
    items["Color"].unique()
)

category_filter = st.sidebar.multiselect(
    "Category",
    items["Category"].unique()
)

# 筛选逻辑
filtered = items.copy()

if brand_filter:
    filtered = filtered[filtered["Brand"].isin(brand_filter)]

if color_filter:
    filtered = filtered[filtered["Color"].isin(color_filter)]

if category_filter:
    filtered = filtered[filtered["Category"].isin(category_filter)]


st.write(f"{len(filtered)} items found")


# 商品网格（淘宝风格）
cols = st.columns(4)

for i, row in filtered.iterrows():

    col = cols[i % 4]

    with col:

        image = Image.open(row["ImagePath"])

        st.image(image, use_container_width=True)

        st.markdown(f"**{row['Name']}**")

        st.write(f"Brand: {row['Brand']}")
        st.write(f"Color: {row['Color']}")

        if st.button("Add to Selection", key=row["ItemID"]):
            st.success("Added")
