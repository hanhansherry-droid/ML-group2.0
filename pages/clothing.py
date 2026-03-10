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
CELEB_PATH = os.path.join(BASE_DIR, "celebrities.xlsx")

HF_BASE = "https://huggingface.co/datasets/sherry2026/fashion-clothing-dataset/resolve/main/"

# ==============================
# SESSION STATE
# ==============================

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "cart" not in st.session_state:
    st.session_state.cart = []

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

        tags.columns = tags.columns.str.strip()

        tags["ItemID"] = tags["ItemID"].astype(str).str.strip()

        return tags

    return pd.DataFrame(columns=["ItemID", "TagType", "Tag"])

tags_df = load_tags()

# ==============================
# LOAD CELEBRITIES
# ==============================

@st.cache_data
def load_celebrities():

    if os.path.exists(CELEB_PATH):

        df = pd.read_excel(CELEB_PATH)

        df.columns = df.columns.str.strip()

        return df

    return pd.DataFrame(columns=["Name","Description","Style Tags"])

celeb_df = load_celebrities()

# ==============================
# GET SELECTED CELEBRITY
# ==============================

selected_celebrity = st.session_state.get("selected_celebrity")

if selected_celebrity is None:

    st.warning("Please select a celebrity first.")

    if st.button("Go to Celebrity Page"):
        st.switch_page("pages/celebrity.py")

    st.stop()

st.success(f"Styling for: {selected_celebrity}")

# ==============================
# GET CELEBRITY STYLE
# ==============================

def get_celebrity_style(name):

    row = celeb_df[celeb_df["Name"] == name]

    if len(row) > 0:

        style = row.iloc[0]["Style Tags"]
        description = row.iloc[0]["Description"]

        return style, description

    return "", ""

style_tags, celebrity_description = get_celebrity_style(selected_celebrity)

st.sidebar.subheader("Celebrity Style")

st.sidebar.write(style_tags)

# ==============================
# LOAD EMBEDDINGS
# ==============================

@st.cache_data
def load_embeddings():
    return np.load(EMBED_PATH)

embeddings = load_embeddings()

item_index_map = {item:idx for idx,item in enumerate(df["ItemID"])}

# ==============================
# IMAGE URL
# ==============================

@st.cache_data
def get_image_url(item_id):

    extensions = [".jpg",".png",".jpeg",".webp"]

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
# SIDEBAR CART
# ==============================

st.sidebar.title("🛍 Stylist Cart")

cart = st.session_state.cart

if len(cart) == 0:
    st.sidebar.write("No items saved")

for i,item in enumerate(cart):

    st.sidebar.image(item["ImageURL"], width=80)

    st.sidebar.markdown(f"**{item['Brand']}**")

    st.sidebar.caption(item["Name"])

    if st.sidebar.button("Remove", key=f"sidebar_remove_{i}"):

        st.session_state.cart.pop(i)

        st.rerun()

st.sidebar.divider()

if st.sidebar.button("Open Cart"):

    st.switch_page("pages/cart.py")

# ==============================
# FILTERS
# ==============================

st.sidebar.header("Filters")

brand_multi = st.sidebar.multiselect(
    "Brand",
    sorted(df["Brand"].dropna().unique())
)

category_multi = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].dropna().unique())
)

color_multi = st.sidebar.multiselect(
    "Color",
    sorted(df["Color"].dropna().unique())
)

occasion_tags = tags_df[tags_df["TagType"]=="Occasion"]["Tag"].unique()
style_tags_filter = tags_df[tags_df["TagType"]=="Style"]["Tag"].unique()

occasion_filter = st.sidebar.multiselect("Occasion", sorted(occasion_tags))
style_filter = st.sidebar.multiselect("Style", sorted(style_tags_filter))

# ==============================
# APPLY FILTER
# ==============================

filtered_df = df.copy()

if brand_multi:
    filtered_df = filtered_df[filtered_df["Brand"].isin(brand_multi)]

if category_multi:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_multi)]

if color_multi:
    filtered_df = filtered_df[filtered_df["Color"].isin(color_multi)]

if occasion_filter:

    item_ids = tags_df[tags_df["Tag"].isin(occasion_filter)]["ItemID"].unique()

    filtered_df = filtered_df[filtered_df["ItemID"].isin(item_ids)]

if style_filter:

    item_ids = tags_df[tags_df["Tag"].isin(style_filter)]["ItemID"].unique()

    filtered_df = filtered_df[filtered_df["ItemID"].isin(item_ids)]

# ==============================
# GRID
# ==============================

st.subheader(f"{len(filtered_df)} items")

cols = st.columns(4)

for i,row in filtered_df.reset_index(drop=True).iterrows():

    with cols[i%4]:

        item_id = row["ItemID"]

        image_url = get_image_url(item_id)

        st.image(image_url, use_container_width=True)

        st.markdown(f"**{row['Brand']}**")

        st.write(row["Name"])

        item_tags = tags_df[tags_df["ItemID"]==item_id]["Tag"].tolist()

        if item_tags:
            st.caption(" ".join([f"#{t}" for t in item_tags]))

        fav_key = f"fav_{item_id}"
        sim_key = f"sim_{item_id}"
        preview_key = f"preview_{item_id}"

        if st.button("Preview", key=preview_key):

            st.session_state.preview_item = row

        if item_id in st.session_state.favorites:

            if st.button("❤️ Remove", key=fav_key):

                st.session_state.favorites.remove(item_id)

                st.session_state.cart = [
                    x for x in st.session_state.cart
                    if x["ItemID"] != item_id
                ]

                st.rerun()

        else:

            if st.button("🤍 Save", key=fav_key):

                st.session_state.favorites.add(item_id)

                cart_item = {
                    "ItemID": item_id,
                    "Brand": row["Brand"],
                    "Name": row["Name"],
                    "ImageURL": image_url,
                    "note": ""
                }

                st.session_state.cart.append(cart_item)

                st.rerun()

        if st.button("Find Similar", key=sim_key):

            idx = item_index_map[item_id]

            query_embedding = embeddings[idx].reshape(1,-1)

            similarity = cosine_similarity(query_embedding, embeddings)[0]

            top_indices = similarity.argsort()[::-1][1:9]

            st.session_state.similar_items = df.iloc[top_indices]

# ==============================
# SIMILAR
# ==============================

if st.session_state.similar_items is not None:

    st.divider()

    st.subheader("Recommended Similar Items")

    cols = st.columns(4)

    for i,row in st.session_state.similar_items.reset_index(drop=True).iterrows():

        with cols[i%4]:

            image_url = get_image_url(row["ItemID"])

            st.image(image_url, use_container_width=True)

            st.markdown(f"**{row['Brand']}**")

            st.write(row["Name"])

    if st.button("Close Similar"):

        st.session_state.similar_items = None

# ==============================
# PREVIEW
# ==============================

if st.session_state.preview_item is not None:

    item = st.session_state.preview_item

    st.divider()

    st.subheader("Item Preview")

    col1,col2 = st.columns([1,1])

    with col1:

        image_url = get_image_url(item["ItemID"])

        st.image(image_url, use_container_width=True)

    with col2:

        st.markdown(f"### {item['Brand']}")

        st.write(item["Name"])

        st.write("Category:", item["Category"])

        st.write("Color:", item["Color"])

        st.write("Season:", item["Season"])

        item_tags = tags_df[tags_df["ItemID"]==item["ItemID"]]["Tag"].tolist()

        if item_tags:

            st.write("Tags:", ", ".join(item_tags))

