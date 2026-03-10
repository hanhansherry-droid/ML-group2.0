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

# ==============================
# PATH
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR,"items.csv")
EMBED_PATH = os.path.join(BASE_DIR,"embeddings","clothing_embeddings.npy")
TAGS_PATH = os.path.join(BASE_DIR,"tags.xlsx")
CELEB_PATH = os.path.join(BASE_DIR,"celebrities.xlsx")

HF_BASE = "https://huggingface.co/datasets/sherry2026/fashion-clothing-dataset/resolve/main/"

# ==============================
# SESSION
# ==============================

if "favorites" not in st.session_state:
    st.session_state.favorites=set()

if "cart" not in st.session_state:
    st.session_state.cart=[]

if "similar_items" not in st.session_state:
    st.session_state.similar_items=None

if "ai_mode" not in st.session_state:
    st.session_state.ai_mode=False

# ==============================
# LOAD CLIP
# ==============================

@st.cache_resource
def load_clip():

    device="cuda" if torch.cuda.is_available() else "cpu"

    model,preprocess=clip.load("ViT-B/32",device=device)

    return model,preprocess,device

model,preprocess,device=load_clip()

# ==============================
# LOAD DATA
# ==============================

@st.cache_data
def load_items():

    df=pd.read_csv(DATA_PATH,encoding="utf-8-sig")
    df.columns=df.columns.str.strip()

    if "No." in df.columns:
        df=df.drop(columns=["No."])

    df["ItemID"]=df["ItemID"].astype(str).str.strip()

    return df

df=load_items()

# ==============================
# TAGS
# ==============================

@st.cache_data
def load_tags():

    if os.path.exists(TAGS_PATH):

        tags=pd.read_excel(TAGS_PATH)
        tags.columns=tags.columns.str.strip()
        tags["ItemID"]=tags["ItemID"].astype(str).str.strip()

        return tags

    return pd.DataFrame(columns=["ItemID","TagType","Tag"])

tags_df=load_tags()

# ==============================
# CELEBRITIES
# ==============================

@st.cache_data
def load_celebrities():

    if os.path.exists(CELEB_PATH):

        df=pd.read_excel(CELEB_PATH)
        df.columns=df.columns.str.strip()

        return df

    return pd.DataFrame(columns=["Name","Description","Style Tags"])

celeb_df=load_celebrities()

# ==============================
# EMBEDDINGS
# ==============================

@st.cache_data
def load_embeddings():

    if os.path.exists(EMBED_PATH):
        return np.load(EMBED_PATH)

    return np.zeros((len(df),512))

embeddings=load_embeddings()

item_index_map={item:idx for idx,item in enumerate(df["ItemID"])}

# ==============================
# CELEBRITY
# ==============================

selected_celebrity=st.session_state.get("selected_celebrity")

if selected_celebrity is None:

    st.warning("Please select a celebrity first")

    if st.button("Go to Celebrity Page"):
        st.switch_page("pages/1_celebrity.py")

    st.stop()

st.success(f"Styling for: {selected_celebrity}")

def get_celebrity_style(name):

    row=celeb_df[celeb_df["Name"]==name]

    if len(row)>0:

        style=row.iloc[0]["Style Tags"]

        return style

    return ""

style_tags=get_celebrity_style(selected_celebrity)

st.sidebar.subheader("Celebrity Style")
st.sidebar.write(style_tags)

# ==============================
# AI IMAGE SEARCH
# ==============================

st.sidebar.divider()
st.sidebar.header("AI Image Search")

uploaded_image=st.sidebar.file_uploader(
"Upload clothing image",
type=["jpg","jpeg","png","webp"]
)

run_ai=st.sidebar.button("Run AI Search")

clear_ai=st.sidebar.button("Clear AI")

# ==============================
# LABEL PREDICTION
# ==============================

def predict(query_embedding,labels):

    tokens=clip.tokenize(labels).to(device)

    with torch.no_grad():
        text_features=model.encode_text(tokens)

    text_features=text_features.cpu().numpy()

    sim=cosine_similarity(query_embedding,text_features)[0]

    return labels[np.argmax(sim)]

style_labels=[
"a photo of elegant fashion",
"a photo of streetwear fashion",
"a photo of sporty outfit",
"a photo of minimal fashion",
"a photo of luxury fashion"
]

occasion_labels=[
"a photo of red carpet outfit",
"a photo of party outfit",
"a photo of casual outfit",
"a photo of office outfit",
"a photo of vacation outfit"
]

color_labels=[
"a photo of black clothing",
"a photo of white clothing",
"a photo of red clothing",
"a photo of pink clothing",
"a photo of blue clothing",
"a photo of beige clothing"
]

pattern_labels=[
"a photo of floral pattern clothing",
"a photo of striped clothing",
"a photo of solid color clothing",
"a photo of graphic print clothing"
]

# ==============================
# RUN AI
# ==============================

if uploaded_image and run_ai:

    image=preprocess(Image.open(uploaded_image).convert("RGB")).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features=model.encode_image(image)

    query_embedding=image_features.cpu().numpy()

    style=predict(query_embedding,style_labels).replace("a photo of ","")
    occasion=predict(query_embedding,occasion_labels).replace("a photo of ","")
    color=predict(query_embedding,color_labels).replace("a photo of ","")
    pattern=predict(query_embedding,pattern_labels).replace("a photo of ","")

    st.session_state.ai_style=style
    st.session_state.ai_occasion=occasion
    st.session_state.ai_color=color
    st.session_state.ai_pattern=pattern

    st.session_state.ai_mode=True

if clear_ai:
    st.session_state.ai_mode=False

# ==============================
# IMAGE URL
# ==============================

@st.cache_data
def get_image_url(item_id):

    extensions=[".jpg",".png",".jpeg",".webp"]

    for ext in extensions:

        url=f"{HF_BASE}{item_id}{ext}"

        try:

            r=requests.head(url,timeout=3)

            if r.status_code==200:
                return url

        except:
            pass

    return "https://via.placeholder.com/400x500?text=No+Image"

# ==============================
# GRID
# ==============================

st.subheader(f"{len(df)} items")

cols=st.columns(4)

for i,row in df.reset_index(drop=True).iterrows():

    with cols[i%4]:

        item_id=row["ItemID"]
        image_url=get_image_url(item_id)

        st.image(image_url,width="stretch")

        st.markdown(f"**{row['Brand']}**")
        st.write(row["Name"])
