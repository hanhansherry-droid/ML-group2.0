import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Fashion Collection", layout="wide")

st.title("Fashion Collection")

# ==============================
# PATH
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "items.csv")

EMBED_PATH = os.path.join(BASE_DIR, "embeddings", "clothing_embeddings.npy")

TAGS_PATH = os.path.join(BASE_DIR, "tags.xlsx")

HF_BASE = "https://huggingface.co/datasets/sherry2026/fashion-clothing-dataset/resolve/main/"

# ==============================
# SESSION STATE
# ==============================

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "preview_item" not in st.session_state:
    st.session_state.preview_item = None

if "similar_items" not in st.session_state:
    st.session_state.similar_items = None

# ==============================
# LOAD ITEMS
# ==============================

@st.cache_data
def load_items():

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    df.columns = df.columns.str.strip()

    if "No." in df.columns:
        df = df.drop(columns=["No."])

    df["ItemID"] = df["ItemID"].astype(str).str.strip()

    return df


df = load_items()

# ==============================
# LOAD TAGS
# ==============================

@st.cache_data
def load_tags():

    if os.path.exists(TAGS_PATH):

        tags = pd.read_excel(TAGS_PATH)

        tags["ItemID"] = tags["ItemID"].astype(str).str.strip()

        return tags

    return pd.DataFrame(columns=["ItemID", "TagType", "Tag"])


tags_df = load_tags()

# ==============================
# LOAD EMBEDDINGS
# ==============================

@st.cache_data
def load_embeddings():

    embeddings = np.load(EMBED_PATH)

    return embeddings


embeddings = load_embeddings()

item_index_map = {item: idx for idx, item in enumerate(df["ItemID"])}

# ==============================
# IMAGE URL (完全不动)
# ==============================

@st.cache_data
def get_image_url(item_id):

    extensions = [".jpg", ".png", ".jpeg", ".webp"]

    for ext in extensions:

        url = f"{HF_BASE}{item_id}{ext}"

        try:
            r = requests.get(url)

            if r.status_code == 200:
                return url

        except:
            pass

    return "https://via.placeholder.com/400x500?text=No+Image"

# ==============================
# SIDEBAR FILTERS
# ==============================

st.sidebar.header("Filters")

brand_multi = st.sidebar.multiselect(
    "Brand",
    options=sorted(df["Brand"].dropna().unique())
)

category_multi = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].dropna().unique())
)

color_multi = st.sidebar.multiselect(
    "Color",
    options=sorted(df["Color"].dropna().unique())
)

# TAG FILTERS

occasion_tags = tags_df[tags_df["TagType"] == "Occasion"]["Tag"].unique()

style_tags = tags_df[tags_df["TagType"] == "Style"]["Tag"].unique()

occasion_filter = st.sidebar.multiselect(
    "Occasion",
    options=sorted(occasion_tags)
)

style_filter = st.sidebar.multiselect(
    "Style",
    options=sorted(style_tags)
)

# ==============================
# APPLY FILTERS
# ==============================

filtered_df = df.copy()

if len(brand_multi) > 0:
    filtered_df = filtered_df[filtered_df["Brand"].isin(brand_multi)]

if len(category_multi) > 0:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_multi)]

if len(color_multi) > 0:
    filtered_df = filtered_df[filtered_df["Color"].isin(color_multi)]

# TAG FILTER

if len(occasion_filter) > 0:

    item_ids = tags_df[
        tags_df["Tag"].isin(occasion_filter)
    ]["ItemID"].unique()

    filtered_df = filtered_df[filtered_df["ItemID"].isin(item_ids)]

if len(style_filter) > 0:

    item_ids = tags_df[
        tags_df["Tag"].isin(style_filter)
    ]["ItemID"].unique()

    filtered_df = filtered_df[filtered_df["ItemID"].isin(item_ids)]

# ==============================
# CLOTHING GRID
# ==============================

st.subheader(f"{len(filtered_df)} items")

cols = st.columns(4)

for i, row in filtered_df.reset_index(drop=True).iterrows():

    with cols[i % 4]:

        item_id = row["ItemID"]

        image_url = get_image_url(item_id)

        st.image(image_url, use_container_width=True)

        st.markdown(f"**{row['Brand']}**")
        st.write(row["Name"])

        # SHOW TAGS

        item_tags = tags_df[tags_df["ItemID"] == item_id]["Tag"].tolist()

        if len(item_tags) > 0:
            st.caption(" ".join([f"#{t}" for t in item_tags]))

        fav_key = f"fav_{item_id}"
        sim_key = f"sim_{item_id}"
        preview_key = f"preview_{item_id}"

        # PREVIEW
        if st.button("Preview", key=preview_key):
            st.session_state.preview_item = row

        # FAVORITES
        if item_id in st.session_state.favorites:

            if st.button("❤️ Remove", key=fav_key):
                st.session_state.favorites.remove(item_id)

        else:

            if st.button("🤍 Save", key=fav_key):
                st.session_state.favorites.add(item_id)

        # SIMILARITY SEARCH
        if st.button("Find Similar", key=sim_key):

            idx = item_index_map[item_id]

            query_embedding = embeddings[idx].reshape(1, -1)

            similarity = cosine_similarity(query_embedding, embeddings)[0]

            top_indices = similarity.argsort()[::-1][1:9]

            st.session_state.similar_items = df.iloc[top_indices]

# ==============================
# SIMILAR ITEMS
# ==============================

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

# ==============================
# PREVIEW SECTION
# ==============================

if st.session_state.preview_item is not None:

    st.divider()

    item = st.session_state.preview_item

    st.subheader("Item Preview")

    col1, col2 = st.columns([1, 1])

    with col1:

        image_url = get_image_url(item["ItemID"])

        st.image(image_url, use_container_width=True)

    with col2:

        st.markdown(f"### {item['Brand']}")
        st.write(item["Name"])

        st.write("Category:", item["Category"])
        st.write("Color:", item["Color"])
        st.write("Season:", item["Season"])

        item_tags = tags_df[tags_df["ItemID"] == item["ItemID"]]["Tag"].tolist()

        if len(item_tags) > 0:
            st.write("Tags:", ", ".join(item_tags))

        if st.button("Close Preview"):
            st.session_state.preview_item = None
