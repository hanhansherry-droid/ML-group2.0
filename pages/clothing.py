import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Fashion Styling", layout="wide")

st.title("AI Fashion Styling Platform")

# ==============================
# BASE DIRECTORY
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# HuggingFace dataset base url
HF_BASE = "https://huggingface.co/datasets/sherry2026/fashion-clothing-dataset/resolve/main/"

# ==============================
# Session State
# ==============================

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "preview_item" not in st.session_state:
    st.session_state.preview_item = None

if "similar_items" not in st.session_state:
    st.session_state.similar_items = None


# ==============================
# Load CSV
# ==============================

@st.cache_data
def load_items():

    path = os.path.join(BASE_DIR, "items.csv")

    df = pd.read_csv(path, encoding="utf-8-sig")

    df.columns = df.columns.str.strip()

    if "No." in df.columns:
        df = df.drop(columns=["No."])

    df["ItemID"] = df["ItemID"].astype(str).str.strip()

    df = df.reset_index(drop=True)

    return df


df = load_items()


# ==============================
# Load Embeddings
# ==============================

@st.cache_data
def load_embeddings():

    path = os.path.join(BASE_DIR, "embeddings", "clothing_embeddings.npy")

    return np.load(path)


embeddings = load_embeddings()

item_index_map = {item: idx for idx, item in enumerate(df["ItemID"])}


# ==============================
# Auto Detect Image URL
# ==============================

@st.cache_data
def get_image_url(item_id):

    extensions = [".jpg", ".png", ".jpeg", ".webp"]

    for ext in extensions:

        url = f"{HF_BASE}{item_id}{ext}"

        try:
            r = requests.head(url)

            if r.status_code == 200:
                return url

        except:
            pass

    return None


# ==============================
# Sidebar Filters
# ==============================

st.sidebar.header("Filters")

brands = ["All"] + sorted(df["Brand"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
colors = ["All"] + sorted(df["Color"].dropna().unique().tolist())

brand_filter = st.sidebar.selectbox("Brand", brands)
category_filter = st.sidebar.selectbox("Category", categories)
color_filter = st.sidebar.selectbox("Color", colors)


# ==============================
# Apply Filters
# ==============================

filtered_df = df.copy()

if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

if color_filter != "All":
    filtered_df = filtered_df[filtered_df["Color"] == color_filter]


# ==============================
# Clothing Grid
# ==============================

st.subheader(f"{len(filtered_df)} items")

cols = st.columns(4)

for i, row in filtered_df.reset_index(drop=True).iterrows():

    with cols[i % 4]:

        item_id = row["ItemID"]

        image_url = get_image_url(item_id)

        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.image(
                "https://via.placeholder.com/400x500?text=No+Image",
                use_container_width=True
            )

        st.markdown(f"**{row['Brand']}**")
        st.write(row["Name"])

        fav_key = f"fav_{i}"
        sim_key = f"sim_{i}"
        preview_key = f"preview_{i}"

        # Preview
        if st.button("Preview", key=preview_key):
            st.session_state.preview_item = row

        # Favorites
        if item_id in st.session_state.favorites:

            if st.button("❤️ Remove", key=fav_key):
                st.session_state.favorites.remove(item_id)

        else:

            if st.button("🤍 Save", key=fav_key):
                st.session_state.favorites.add(item_id)

        # Find Similar
        if st.button("Find Similar", key=sim_key):

            idx = item_index_map[item_id]

            query_embedding = embeddings[idx].reshape(1, -1)

            similarity = cosine_similarity(query_embedding, embeddings)[0]

            top_indices = similarity.argsort()[::-1][1:9]

            st.session_state.similar_items = df.iloc[top_indices]


# ==============================
# Similar Items
# ==============================

if st.session_state.similar_items is not None:

    st.divider()

    st.subheader("Recommended Similar Items")

    sim_df = st.session_state.similar_items

    cols = st.columns(4)

    for i, row in sim_df.reset_index(drop=True).iterrows():

        with cols[i % 4]:

            image_url = get_image_url(row["ItemID"])

            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.image(
                    "https://via.placeholder.com/400x500",
                    use_container_width=True
                )

            st.markdown(f"**{row['Brand']}**")
            st.write(row["Name"])


# ==============================
# Preview Section
# ==============================

if st.session_state.preview_item is not None:

    st.divider()

    item = st.session_state.preview_item

    st.subheader("Item Preview")

    col1, col2 = st.columns([1,1])

    with col1:

        image_url = get_image_url(item["ItemID"])

        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.image(
                "https://via.placeholder.com/400x500",
                use_container_width=True
            )

    with col2:

        st.markdown(f"### {item['Brand']}")

        st.write(item["Name"])

        st.write("Category:", item["Category"])
        st.write("Color:", item["Color"])
        st.write("Season:", item["Season"])

        if st.button("Close Preview"):
            st.session_state.preview_item = None
