import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import torch
import clip

from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Fashion Collection", layout="wide")
st.title("Fashion Collection")

# ======================
# PATH
# ======================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR,"items.csv")
EMBED_PATH = os.path.join(BASE_DIR,"embeddings","clothing_embeddings.npy")
TAGS_PATH = os.path.join(BASE_DIR,"tags.xlsx")
CELEB_PATH = os.path.join(BASE_DIR,"celebrities.xlsx")

HF_BASE = "https://huggingface.co/datasets/sherry2026/fashion-clothing-dataset/resolve/main/"

# ======================
# SESSION STATE
# ======================

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "preview_item" not in st.session_state:
    st.session_state.preview_item = None

if "similar_items" not in st.session_state:
    st.session_state.similar_items = None

if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = False

# ======================
# LOAD CLIP
# ======================

@st.cache_resource
def load_clip():

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model, preprocess = clip.load("ViT-B/32", device=device)

    return model, preprocess, device


model, preprocess, device = load_clip()

# ======================
# LOAD DATA
# ======================

@st.cache_data
def load_items():

    df = pd.read_csv(DATA_PATH,encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    if "No." in df.columns:
        df = df.drop(columns=["No."])

    df["ItemID"] = df["ItemID"].astype(str).str.strip()

    return df


df = load_items()

@st.cache_data
def load_tags():

    if os.path.exists(TAGS_PATH):

        tags = pd.read_excel(TAGS_PATH)
        tags.columns = tags.columns.str.strip()
        tags["ItemID"] = tags["ItemID"].astype(str).str.strip()

        return tags

    return pd.DataFrame(columns=["ItemID","TagType","Tag"])


tags_df = load_tags()

@st.cache_data
def load_celebrities():

    if os.path.exists(CELEB_PATH):

        df = pd.read_excel(CELEB_PATH)
        df.columns = df.columns.str.strip()

        return df

    return pd.DataFrame(columns=["Name","Description","Style Tags"])


celeb_df = load_celebrities()

# ======================
# LOAD EMBEDDINGS
# ======================

@st.cache_data
def load_embeddings():
    return np.load(EMBED_PATH)

embeddings = load_embeddings()

item_index_map = {item:idx for idx,item in enumerate(df["ItemID"])}

# ======================
# GET CELEBRITY
# ======================

selected_celebrity = st.session_state.get("selected_celebrity")

if selected_celebrity is None:

    st.warning("Please select a celebrity first")

    if st.button("Go to Celebrity Page"):
        st.switch_page("pages/1_celebrity.py")

    st.stop()

st.success(f"Styling for: {selected_celebrity}")

def get_celebrity_style(name):

    row = celeb_df[celeb_df["Name"] == name]

    if len(row)>0:

        style = row.iloc[0]["Style Tags"]
        description = row.iloc[0]["Description"]

        return style, description

    return "", ""

style_tags, celebrity_description = get_celebrity_style(selected_celebrity)

st.sidebar.subheader("Celebrity Style")
st.sidebar.write(style_tags)

# ======================
# AI IMAGE SEARCH
# ======================

st.sidebar.divider()
st.sidebar.header("AI Image Search")

uploaded_image = st.sidebar.file_uploader(
    "Upload clothing image",
    type=["jpg","jpeg","png","webp"]
)

run_ai = st.sidebar.button("Run AI Search")
clear_ai = st.sidebar.button("Clear AI Search")

# ======================
# AI LABEL PREDICT
# ======================

def predict_label(query_embedding, labels):

    tokens = clip.tokenize(labels).to(device)

    with torch.no_grad():

        text_features = model.encode_text(tokens)

    text_features = text_features.cpu().numpy()

    sim = cosine_similarity(query_embedding,text_features)[0]

    return labels[np.argmax(sim)]


style_labels = [
"a photo of elegant fashion",
"a photo of streetwear fashion",
"a photo of sporty outfit",
"a photo of minimal fashion",
"a photo of luxury fashion"
]

occasion_labels = [
"a photo of red carpet outfit",
"a photo of party outfit",
"a photo of casual outfit",
"a photo of office outfit",
"a photo of vacation outfit"
]

# ======================
# RUN AI SEARCH
# ======================

if uploaded_image and run_ai:

    image = preprocess(Image.open(uploaded_image)).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)

    query_embedding = image_features.cpu().numpy()

    style = predict_label(query_embedding,style_labels)
    occasion = predict_label(query_embedding,occasion_labels)

    style = style.replace("a photo of ","")
    occasion = occasion.replace("a photo of ","")

    st.session_state.ai_style = style
    st.session_state.ai_occasion = occasion
    st.session_state.ai_mode = True

if clear_ai:

    st.session_state.ai_mode = False

# ======================
# APPLY FILTER
# ======================

filtered_df = df.copy()

if st.session_state.ai_mode:

    st.sidebar.subheader("AI Recognition")

    st.sidebar.write("Style:",st.session_state.ai_style)
    st.sidebar.write("Occasion:",st.session_state.ai_occasion)

    style_items = tags_df[
        tags_df["Tag"]==st.session_state.ai_style
    ]["ItemID"]

    occasion_items = tags_df[
        tags_df["Tag"]==st.session_state.ai_occasion
    ]["ItemID"]

    matched_ids = set(style_items).intersection(set(occasion_items))

    filtered_df = df[df["ItemID"].isin(matched_ids)]

# ======================
# CELEBRITY STYLE BOOST
# ======================

if style_tags:

    celeb_styles = [s.strip() for s in style_tags.split(",")]

    celeb_items = tags_df[
        tags_df["Tag"].isin(celeb_styles)
    ]["ItemID"].unique()

    celeb_df_filtered = df[df["ItemID"].isin(celeb_items)]

    filtered_df = pd.concat([celeb_df_filtered,filtered_df]).drop_duplicates()

# ======================
# IMAGE URL
# ======================

@st.cache_data
def get_image_url(item_id):

    extensions = [".jpg",".png",".jpeg",".webp"]

    for ext in extensions:

        url = f"{HF_BASE}{item_id}{ext}"

        try:

            r = requests.get(url,timeout=3)

            if r.status_code==200:
                return url

        except:
            pass

    return "https://via.placeholder.com/400x500?text=No+Image"

# ======================
# GRID
# ======================

st.subheader(f"{len(filtered_df)} items")

cols = st.columns(4)

for i,row in filtered_df.reset_index(drop=True).iterrows():

    with cols[i%4]:

        item_id = row["ItemID"]
        image_url = get_image_url(item_id)

        st.image(image_url,use_container_width=True)

        st.markdown(f"**{row['Brand']}**")
        st.write(row["Name"])

        item_tags = tags_df[tags_df["ItemID"]==item_id]["Tag"].tolist()

        if item_tags:
            st.caption(" ".join([f"#{t}" for t in item_tags]))

        if st.button("Preview",key=f"preview_{item_id}"):

            st.session_state.preview_item = row

        if item_id in st.session_state.favorites:

            if st.button("❤️ Remove",key=f"remove_{item_id}"):

                st.session_state.favorites.remove(item_id)

                st.session_state.cart = [
                    x for x in st.session_state.cart
                    if x["ItemID"] != item_id
                ]

                st.rerun()

        else:

            if st.button("🤍 Save",key=f"save_{item_id}"):

                st.session_state.favorites.add(item_id)

                cart_item = {
                    "ItemID": item_id,
                    "Brand": row["Brand"],
                    "Name": row["Name"],
                    "ImageURL": image_url,
                    "note":""
                }

                st.session_state.cart.append(cart_item)

                st.rerun()

        if st.button("Find Similar",key=f"sim_{item_id}"):

            idx = item_index_map.get(item_id)

            if idx is not None:

                query_embedding = embeddings[idx].reshape(1,-1)

                similarity = cosine_similarity(query_embedding,embeddings)[0]

                top_indices = similarity.argsort()[::-1][1:9]

                st.session_state.similar_items = df.iloc[top_indices]

# ======================
# SIMILAR
# ======================

if st.session_state.similar_items is not None:

    st.divider()
    st.subheader("Recommended Similar Items")

    cols = st.columns(4)

    for i,row in st.session_state.similar_items.reset_index(drop=True).iterrows():

        with cols[i%4]:

            image_url = get_image_url(row["ItemID"])

            st.image(image_url,use_container_width=True)

            st.markdown(f"**{row['Brand']}**")
            st.write(row["Name"])

    if st.button("Close Similar"):

        st.session_state.similar_items = None
