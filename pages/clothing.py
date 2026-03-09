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

@st.cache_data
def load_items():
    df = pd.read_excel("items.xlsx")
    df.columns = df.columns.str.strip()

    # 清洗 ItemID
    df["ItemID"] = df["ItemID"].astype(str)
    df = df[df["ItemID"] != "nan"]

    df = df.reset_index(drop=True)

    return df

df = load_items()

# ======================
# Load embeddings
# ======================

@st.cache_data
def load_embeddings():
    return np.load("embeddings/clothing_embeddings.npy")

embeddings = load_embeddings()

# 建立 ItemID → embedding index 映射
item_index_map = {item: idx for idx, item in enumerate(df["ItemID"])}

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

for i, row in filtered_df.reset_index(drop=True).iterrows():

    with cols[i % 4]:

        item_id = row["ItemID"]

        image_path = os.path.join("images", f"{item_id}.jpg")

        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.empty()

        st.markdown(f"**{row['Brand']}**")
        st.write(row["Name"])

        # 唯一 key（只用 index）
        fav_key = f"favorite_button_{i}"
        sim_key = f"similar_button_{i}"

        # ======================
        # Favorite
        # ======================

        if item_id in st.session_state.favorites:

            if st.button("❤️ Remove", key=fav_key):
                st.session_state.favorites.remove(item_id)

        else:

            if st.button("🤍 Save", key=fav_key):
                st.session_state.favorites.add(item_id)

        # ======================
        # Find Similar
        # ======================

        if st.button("Find Similar", key=sim_key):

    idx = item_index_map[item_id]

    query_embedding = embeddings[idx].reshape(1, -1)

    similarity = cosine_similarity(query_embedding, embeddings)[0]

    top_indices = similarity.argsort()[::-1][1:5]

    st.write("Similar items:")

    for j in top_indices:

        # 防止 index 超出 df
        if j >= len(df):
            continue

        sim_item = df.iloc[j]

        sim_image = os.path.join("images", f"{sim_item['ItemID']}.jpg")

        if os.path.exists(sim_image):
            st.image(sim_image, width=120)

        st.write(sim_item["Brand"], "-", sim_item["Name"])

