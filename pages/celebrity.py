import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Select Celebrity", layout="wide")

st.title("Select Celebrity")

# ======================
# PATH
# ======================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELEB_PATH = os.path.join(BASE_DIR, "celebrities.xlsx")

# HuggingFace base path
HF_BASE = "https://huggingface.co/datasets/sherry2026/celebrity/resolve/main/"

# ======================
# Load data
# ======================

@st.cache_data
def load_celebrities():
    
    df = pd.read_excel(CELEB_PATH)
    
    df.columns = df.columns.str.strip()
    
    # 保证 URL 为字符串
    if "ImageURL" in df.columns:
        df["ImageURL"] = df["ImageURL"].astype(str).str.strip()
    
    return df


celeb_df = load_celebrities()

# ======================
# Session state
# ======================

if "selected_celebrity" not in st.session_state:
    st.session_state.selected_celebrity = None

# ======================
# Celebrity cards
# ======================

cols = st.columns(3)

for i, row in celeb_df.iterrows():

    with cols[i % 3]:

        name = row["Name"]
        description = row["Description"]
        style = row["Style Tags"]
        image_url = row["ImageURL"]

        st.subheader(name)

        # 显示图片
        if isinstance(image_url, str) and image_url.startswith("http"):
            st.image(image_url, use_container_width=True)
        else:
            st.warning("Image not available")

        # Style tags
        st.caption(style)

        # Description
        st.write(description)

        # Select button
        if st.button("Select", key=name):

            st.session_state.selected_celebrity = name
            st.success(f"Selected: {name}")

# ======================
# Continue system
# ======================

st.divider()

if st.session_state.selected_celebrity:

    st.write("Selected Celebrity:", st.session_state.selected_celebrity)

    if st.button("Continue to Clothing"):

        st.switch_page("pages/clothing.py")

else:

    st.info("Please select a celebrity to continue.")

else:

    st.info("Please select a celebrity to continue.")

