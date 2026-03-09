import streamlit as st
import pandas as pd
import os
import numpy as np
import torch
import clip
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Clothing Collection",
    layout="wide"
)

# ======================
# UI STYLE
# ======================

st.markdown("""
<style>

.stApp {
    background-color: #fafafa;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

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

# ======================
# Load embeddings
# ======================

embeddings = np.load("embeddings/clothing_embeddings.npy")

# ======================
# Load CLIP model
# ======================

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# ======================
# AI Search
# ======================

st.subheader("AI Search")

query = st.text_input("Describe clothing style")

search_clicked = st.button("Search")

if search_clicked and query:

    text = clip.tokenize([query]).to(device)

    with torch.no_grad():
        text_features = model.encode_text(text)

    text_embedding = text_features.cpu().numpy()

    similarity = cosine_similarity(text_embedding, embeddings)[0]

    top_indices = similarity.argsort()[::-1][:12]

    filtered_df = df.iloc[top_indices]

else:
    filtered_df = df.copy()

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
            if st.button("❤️", key=f"fav_{item_id}"):
                st.session_state.favorites.remove(item_id)
        else:
            if st.button("🤍", key=f"fav_{item_id}"):
                st.session_state.favorites.add(item_id)

        # ======================
        # Find Similar
        # ======================

        if st.button("Find Similar", key=f"sim_{item_id}"):

            idx = df[df["ItemID"] == item_id].index[0]

            query_embedding = embeddings[idx].reshape(1, -1)

            similarity = cosine_similarity(query_embedding, embeddings)[0]

            top_indices = similarity.argsort()[::-1][1:5]

            st.write("Similar items:")

            for j in top_indices:
                sim_item = df.iloc[j]

                st.write(
                    sim_item["Brand"],
                    "-",
                    sim_item["Name"]
                )

