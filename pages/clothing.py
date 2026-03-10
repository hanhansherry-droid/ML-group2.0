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
    st.session_state.favorites=set()

if "preview_item" not in st.session_state:
    st.session_state.preview_item=None

if "similar_items" not in st.session_state:
    st.session_state.similar_items=None

# ==============================
# LOAD ITEMS
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
# LOAD TAGS
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
# LOAD CELEBRITIES
# ==============================

@st.cache_data
def load_celebrities():

    if not os.path.exists(CELEB_PATH):

        return pd.DataFrame(columns=["Name","Description","Style Tags"])

    df=pd.read_excel(CELEB_PATH)

    df.columns=df.columns.str.strip()

    return df

celeb_df=load_celebrities()

# ==============================
# LOAD EMBEDDINGS
# ==============================

@st.cache_data
def load_embeddings():

    return np.load(EMBED_PATH)

embeddings=load_embeddings()

item_index_map={item:idx for idx,item in enumerate(df["ItemID"])}

# ==============================
# IMAGE URL (保持原逻辑)
# ==============================

@st.cache_data
def get_image_url(item_id):

    extensions=[".jpg",".png",".jpeg",".webp"]

    for ext in extensions:

        url=f"{HF_BASE}{item_id}{ext}"

        try:

            r=requests.get(url)

            if r.status_code==200:
                return url

        except:
            pass

    return "https://via.placeholder.com/400x500?text=No+Image"

# ==============================
# SIDEBAR FILTERS
# ==============================

st.sidebar.header("Filters")

brand_multi=st.sidebar.multiselect(
    "Brand",
    sorted(df["Brand"].dropna().unique())
)

category_multi=st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].dropna().unique())
)

color_multi=st.sidebar.multiselect(
    "Color",
    sorted(df["Color"].dropna().unique())
)

# TAG FILTER

occasion_tags=tags_df[tags_df["TagType"]=="Occasion"]["Tag"].unique()
style_tags=tags_df[tags_df["TagType"]=="Style"]["Tag"].unique()

occasion_filter=st.sidebar.multiselect("Occasion",sorted(occasion_tags))
style_filter=st.sidebar.multiselect("Style",sorted(style_tags))

# ==============================
# CELEBRITY SELECTOR
# ==============================

celebrity_list=celeb_df["Name"].dropna().unique().tolist()

celebrity=st.sidebar.selectbox("Celebrity",celebrity_list)

# ==============================
# APPLY FILTER
# ==============================

filtered_df=df.copy()

if brand_multi:
    filtered_df=filtered_df[filtered_df["Brand"].isin(brand_multi)]

if category_multi:
    filtered_df=filtered_df[filtered_df["Category"].isin(category_multi)]

if color_multi:
    filtered_df=filtered_df[filtered_df["Color"].isin(color_multi)]

if occasion_filter:

    item_ids=tags_df[
        tags_df["Tag"].isin(occasion_filter)
    ]["ItemID"].unique()

    filtered_df=filtered_df[
        filtered_df["ItemID"].isin(item_ids)
    ]

if style_filter:

    item_ids=tags_df[
        tags_df["Tag"].isin(style_filter)
    ]["ItemID"].unique()

    filtered_df=filtered_df[
        filtered_df["ItemID"].isin(item_ids)
    ]

# ==============================
# GET CELEBRITY STYLE
# ==============================

def get_celebrity_style(name):

    row=celeb_df[celeb_df["Name"]==name]

    if len(row)>0:

        description=row.iloc[0]["Description"]
        style=row.iloc[0]["Style Tags"]

        return style,description

    return "",""

# ==============================
# AI STYLIST
# ==============================

def ai_agent(filtered_items):

    if "huggingface" not in st.secrets:

        return "⚠️ HuggingFace API key not configured."

    api_key=st.secrets["huggingface"].get("api_key","")

    if api_key=="":
        return "⚠️ HuggingFace API key missing."

    if len(filtered_items)==0:
        return "No clothing items match the filters."

    style_hint,celeb_description=get_celebrity_style(celebrity)

    brands=", ".join(filtered_items["Brand"].unique()[:5])
    categories=", ".join(filtered_items["Category"].unique()[:5])
    colors=", ".join(filtered_items["Color"].unique()[:5])

    prompt=f"""
You are a professional celebrity fashion stylist.

Celebrity: {celebrity}

Celebrity style tags:
{style_hint}

Celebrity description:
{celeb_description}

Filters:
Brand: {brand_multi}
Category: {category_multi}
Color: {color_multi}
Occasion: {occasion_filter}
Style: {style_filter}

Available inventory:
Brands: {brands}
Categories: {categories}
Colors: {colors}

Recommend clothing items suitable for the celebrity and explain why.
"""

    headers={"Authorization":f"Bearer {api_key}"}

    payload={
        "inputs":prompt,
        "parameters":{"max_new_tokens":200}
    }

    try:

        response=requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code!=200:
            return f"API error {response.status_code}"

        result=response.json()

        if isinstance(result,list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        if isinstance(result,dict) and "generated_text" in result:
            return result["generated_text"]

        return str(result)

    except Exception as e:

        return f"AI error: {e}"

# ==============================
# AI BUTTON
# ==============================

if st.sidebar.button("Generate AI Styling Advice"):

    with st.sidebar.spinner("AI stylist thinking..."):

        advice=ai_agent(filtered_df)

    st.sidebar.success("Styling Advice")

    st.sidebar.write(advice)

# ==============================
# GRID
# ==============================

st.subheader(f"{len(filtered_df)} items")

cols=st.columns(4)

for i,row in filtered_df.reset_index(drop=True).iterrows():

    with cols[i%4]:

        item_id=row["ItemID"]

        image_url=get_image_url(item_id)

        st.image(image_url,use_container_width=True)

        st.markdown(f"**{row['Brand']}**")
        st.write(row["Name"])

        item_tags=tags_df[tags_df["ItemID"]==item_id]["Tag"].tolist()

        if item_tags:
            st.caption(" ".join([f"#{t}" for t in item_tags]))

        fav_key=f"fav_{item_id}"
        sim_key=f"sim_{item_id}"
        preview_key=f"preview_{item_id}"

        if st.button("Preview",key=preview_key):
            st.session_state.preview_item=row

        if item_id in st.session_state.favorites:
            if st.button("❤️ Remove",key=fav_key):
                st.session_state.favorites.remove(item_id)
        else:
            if st.button("🤍 Save",key=fav_key):
                st.session_state.favorites.add(item_id)

        if st.button("Find Similar",key=sim_key):

            idx=item_index_map[item_id]

            query_embedding=embeddings[idx].reshape(1,-1)

            similarity=cosine_similarity(query_embedding,embeddings)[0]

            top_indices=similarity.argsort()[::-1][1:9]

            st.session_state.similar_items=df.iloc[top_indices]

# ==============================
# SIMILAR
# ==============================

if st.session_state.similar_items is not None:

    st.divider()

    st.subheader("Recommended Similar Items")

    cols=st.columns(4)

    for i,row in st.session_state.similar_items.reset_index(drop=True).iterrows():

        with cols[i%4]:

            image_url=get_image_url(row["ItemID"])

            st.image(image_url,use_container_width=True)

            st.markdown(f"**{row['Brand']}**")
            st.write(row["Name"])

    if st.button("Close Similar"):
        st.session_state.similar_items=None

# ==============================
# PREVIEW
# ==============================

if st.session_state.preview_item is not None:

    item=st.session_state.preview_item

    st.divider()

    st.subheader("Item Preview")

    col1,col2=st.columns([1,1])

    with col1:

        image_url=get_image_url(item["ItemID"])
        st.image(image_url,use_container_width=True)

    with col2:

        st.markdown(f"### {item['Brand']}")
        st.write(item["Name"])

        st.write("Category:",item["Category"])
        st.write("Color:",item["Color"])
        st.write("Season:",item["Season"])

        item_tags=tags_df[tags_df["ItemID"]==item["ItemID"]]["Tag"].tolist()

        if item_tags:
            st.write("Tags:",", ".join(item_tags))

        if st.button("Close Preview"):
            st.session_state.preview_item=None
