import streamlit as st
import pandas as pd
import numpy as np
import os
import torch
import clip
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Collection", layout="wide")

st.title("Fashion Collection")

# 初始化 styling board
if "board" not in st.session_state:
    st.session_state.board = []

# =========================
# Load dataset
# =========================

@st.cache_data
def load_items():
    df = pd.read_excel("items.xlsx")
    df.columns = df.columns.str.strip()
    df["ItemID"] = df["ItemID"].astype(str)
    df = df[df["ItemID"] != "nan"]
    df = df.reset_index(drop=True)
    return df

df = load_items()

# =========================
# Load embeddings
# =========================

@st.cache_data
def load_embeddings():
    return np.load("embeddings/clothing_embeddings.npy")

embeddings = load_embeddings()

# =========================
# Load CLIP
# =========================

@st.cache_resource
def load_clip():
    device = "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, device

model, device = load_clip()

# =========================
# AI Search
# =========================

st.subheader("AI Styling Search")

query = st.text_input(
    "Describe the style or occasion",
    placeholder="e.g. korean streetwear for concert"
)

search = st.button("Search")

if search and query != "":

    text = clip.tokenize([query]).to(device)

    with torch.no_grad():
        text_features = model.encode_text(text)

    text_embedding = text_features.cpu().numpy()

    similarity = cosine_similarity(text_embedding, embeddings)[0]

    top_indices = similarity.argsort()[::-1][:8]

    st.subheader("Recommended Pieces")

    cols = st.columns(4)

    for i, idx in enumerate(top_indices):

        if idx >= len(df):
            continue

        row = df.iloc[idx]

        with cols[i % 4]:

            image_path = os.path.join("images", f"{row['ItemID']}.jpg")

            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)

            st.markdown(f"**{row['Brand']}**")
            st.write(row["Name"])

            if st.button("Add to Styling Board", key=f"ai_{idx}"):

                st.session_state.board.append(row["ItemID"])

# =========================
# Browse Collection
# =========================

st.subheader("Browse Collection")

cols = st.columns(4)

for i, row in df.iterrows():

    with cols[i % 4]:

        image_path = os.path.join("images", f"{row['ItemID']}.jpg")

        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)

        st.markdown(f"**{row['Brand']}**")
        st.write(row["Name"])

        if st.button("Add to Styling Board", key=f"browse_{i}"):

            st.session_state.board.append(row["ItemID"])
