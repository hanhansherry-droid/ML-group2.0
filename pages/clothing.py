import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Clothing Collection",
    layout="wide"
)

st.title("New Collection")

# ======================
# Favorites storage
# ======================

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# ======================
# Load dataset
# ======================

df = pd.read_excel("items.xlsx")
df.columns = df.columns.str.strip()

# load embeddings
embeddings = np.load("embeddings/clothing_embeddings.npy")

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

        # brand
        st.markdown(f"**{row['Brand']}**")

        # item name
        st.write(row["Name"])

        item_id = row["ItemID"]

        # ======================
        # Favorite button
        # ======================

        if item_id in st.session_state.favorites:
            if st.button("❤️ Remove", key=f"fav_{item_id}"):
                st.session_state.favorites.remove(item_id)
        else:
            if st.button("🤍 Save", key=f"fav_{item_id}"):
                st.session_state.favorites.add(item_id)

        # ======================
        # Similar items
        # ======================

        if st.button("Find Similar", key=f"sim_{item_id}"):

            idx = df[df["ItemID"] == item_id].index[0]

            query_embedding = embeddings[idx].reshape(1, -1)

            similarity = cosine_similarity(query_embedding, embeddings)[0]

            top_indices = similarity.argsort()[::-1][1:5]

            st.write("Similar items:")

            for j in top_indices:
                st.write(df.iloc[j]["ItemID"], "-", df.iloc[j]["Brand"])


