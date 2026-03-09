import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Clothing Collection",
    layout="wide"
)

st.title("New Collection")

# ======================
# Load dataset
# ======================

df = pd.read_excel("items.xlsx")

# 防止列名有空格
df.columns = df.columns.str.strip()

# ======================
# Sidebar Filters
# ======================

st.sidebar.header("Filters")

brands = ["All"] + sorted(df["Brand"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
colors = ["All"] + sorted(df["Color"].dropna().unique().tolist())

brand_filter = st.sidebar.selectbox("Brand", brands)
category_filter = st.sidebar.selectbox("Category", categories)
color_filter = st.sidebar.selectbox("Color", colors)

# ======================
# Apply filters
# ======================

filtered_df = df.copy()

if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

if color_filter != "All":
    filtered_df = filtered_df[filtered_df["Color"] == color_filter]

st.write(f"{len(filtered_df)} items found")

# ======================
# Clothing Grid
# ======================

cols = st.columns(4)

for i, row in filtered_df.iterrows():

    with cols[i % 4]:

        image_path = os.path.join("images", f"{row['ItemID']}.jpg")

        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.write("Image not found")

        # 品牌（黑色加粗）
        st.markdown(f"**{row['Brand']}**")

        # Item描述
        st.write(row["Name"])

