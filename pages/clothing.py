import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Clothing Collection",
    layout="wide"
)

st.title("Clothing Collection")

st.write("Browse the fashion database.")

# ======================
# Load data
# ======================

df = pd.read_excel("items.xlsx")

# ======================
# Filters
# ======================

st.sidebar.header("Filters")

brand_filter = st.sidebar.selectbox(
    "Brand",
    ["All"] + sorted(df["Brand"].unique().tolist())
)

category_filter = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

color_filter = st.sidebar.selectbox(
    "Color",
    ["All"] + sorted(df["Color"].unique().tolist())
)

# Apply filters

filtered_df = df.copy()

if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

if color_filter != "All":
    filtered_df = filtered_df[filtered_df["Color"] == color_filter]

# ======================
# Clothing grid
# ======================

cols = st.columns(4)

for i, row in filtered_df.iterrows():

    with cols[i % 4]:

        image_path = os.path.join("images", f"{row['ItemID']}.jpg")

        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.write("Image not found")

        st.markdown(f"**{row['Name']}**")
        st.caption(row["Brand"])

        st.write(f"Category: {row['Category']}")
        st.write(f"Color: {row['Color']}")
