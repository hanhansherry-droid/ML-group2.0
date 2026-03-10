import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Select Celebrity", layout="wide")

st.title("Select Celebrity")

# ======================
# Load celebrity data
# ======================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELEB_PATH = os.path.join(BASE_DIR, "celebrities.xlsx")

@st.cache_data
def load_celebrities():
    df = pd.read_excel(CELEB_PATH)
    df.columns = df.columns.str.strip()

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
# Celebrity list
# ======================

cols = st.columns(3)

for i, row in celeb_df.iterrows():

    with cols[i % 3]:

        st.subheader(row["Name"])

        # ===== safer image loading =====
        if "ImageURL" in celeb_df.columns:

            url = row["ImageURL"]

            try:
                if isinstance(url, str) and url.startswith("http"):

                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_container_width=True)

                else:
                    st.warning("Image not available")

            except:
                st.warning("Image failed to load")

        st.write(row["Description"])

        if st.button("Select", key=row["Name"]):

            st.session_state.selected_celebrity = row["Name"]
            st.success(f"Selected: {row['Name']}")

# ======================
# Continue button
# ======================

st.divider()

if st.session_state.selected_celebrity:

    st.write("Selected:", st.session_state.selected_celebrity)

    if st.button("Continue to Clothing"):
        st.switch_page("pages/clothing.py")

else:

    st.info("Please select a celebrity.")
