import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Fashion Collection", layout="wide")

st.title("Fashion Collection")

# =====================================
# BASE DIRECTORY
# =====================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "items.csv")

EMBED_PATH = os.path.join(BASE_DIR, "embeddings", "clothing_embeddings.npy")

HF_BASE = "https://huggingface.co/datasets/sherry2026/fashion-clothing-dataset/resolve/main/"

# =====================================
# Session State
# =====================================

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "preview_item" not in st.session_state:
    st.session_state.preview_item = None

if "similar_items" not in st.session_state:
    st.session_state.similar_items = None


# =====================================
# Load Items
# =====================================

@st.cache_data
def load_items():

    if not os.path.exists(DATA_PATH):
        st.error(f"items.csv not found: {DATA_PATH}")
        st.stop()

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    df.columns = df.columns.str.strip()

    if "No." in df.columns:
        df = df.drop(columns=["No."])

    df["ItemID"] = df["ItemID"].astype(str).str.strip()

    return df


df = load_items()


# =====================================
# Load Embeddings
# =====================================

@st.cache_data
def load_embeddings():

    if not os.path.exists(EMBED_PATH):
        st.error(f"Embedding file not found: {EMBED_PATH}")
        st.stop()

    embeddings = np.load(EMBED_PATH)

    return embeddings


embeddings = load_embeddings()

item_index_map = {item: idx for idx, item in enumerate(df["ItemID"])}


# =====================================
# Image URL
# =====================================

def get_image_url(item_id):

    return f"{HF_BASE}{item_id}.jpg"


# =====================================
# Sidebar Filters
# =====================================

st.sidebar.header("Filters")

brands = ["All"] + sorted(df["Brand"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
colors = ["All"] + sorted(df["Color"].dropna().unique().tolist())

brand_filter = st.sidebar.selectbox("Brand", brands)
category_filter = st.sidebar.selectbox("Category", categories)
color_filter = st.sidebar.selectbox("Color", colors)


# =====================================
# Apply Filters
# =====================================

filtered_df = df.copy()

if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

if color_filter != "All":
    filtered_df = filtered_df[filtered_df["Color"] == color_filter]


# =====================================
# Clothing Grid
# =====================================

st.subheader(f"{len(filtered_df)} items")

cols = st.columns(4)

for i, row in filtered_df.reset_index(drop=True).iterrows():

    with cols[i % 4]:

        item_id = row["ItemID"]

        image_url = get_image_url(item_id)

        st.image(image_url, use_container_width=True)

        st.markdown(f"**{row['Brand']}**")

        st.write(row["Name"])

        fav_key = f"fav_{item_id}"
        sim_key = f"sim_{item_id}"
        preview_key = f"preview_{item_id}"


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


        # Similar
        if st.button("Find Similar", key=sim_key):

            idx = item_index_map[item_id]

            query_embedding = embeddings[idx].reshape(1, -1)

            similarity = cosine_similarity(query_embedding, embeddings)[0]

            top_indices = similarity.argsort()[::-1][1:9]

            st.session_state.similar_items = df.iloc[top_indices]


# =====================================
# Similar Items
# =====================================

if st.session_state.similar_items is not None:

    st.divider()

    st.subheader("Recommended Similar Items")

    sim_df = st.session_state.similar_items

    cols = st.columns(4)

    for i, row in sim_df.reset_index(drop=True).iterrows():

        with cols[i % 4]:

            image_url = get_image_url(row["ItemID"])

            st.image(image_url, use_container_width=True)

            st.markdown(f"**{row['Brand']}**")

            st.write(row["Name"])


# =====================================
# Preview
# =====================================

if st.session_state.preview_item is not None:

    st.divider()

    item = st.session_state.preview_item

    st.subheader("Item Preview")

    col1, col2 = st.columns([1,1])

    with col1:

        image_url = get_image_url(item["ItemID"])

        st.image(image_url, use_container_width=True)

    with col2:

        st.markdown(f"### {item['Brand']}")

        st.write(item["Name"])

        st.write("Category:", item["Category"])
        st.write("Color:", item["Color"])
        st.write("Season:", item["Season"])

        if st.button("Close Preview"):
            st.session_state.preview_item = None
