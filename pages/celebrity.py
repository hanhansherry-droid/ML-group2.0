import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Select Celebrity", layout="wide")

st.title("Select Celebrity")

# ======================
# PATH
# ======================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELEB_PATH = os.path.join(BASE_DIR, "celebrities.xlsx")

# ======================
# Load data
# ======================

@st.cache_data
def load_celebrities():

    df = pd.read_excel(CELEB_PATH)

    df.columns = df.columns.str.strip()

    if "ImageURL" in df.columns:
        df["ImageURL"] = df["ImageURL"].astype(str).str.strip()

    return df

celeb_df = load_celebrities()

st.write("Loaded columns:", celeb_df.columns.tolist())
st.write("Total celebrities:", len(celeb_df))


# ======================
# Session state
# ======================

if "selected_celebrity" not in st.session_state:
    st.session_state.selected_celebrity = None


# ======================
# Celebrity display
# ======================

cols = st.columns(3)

for i, row in celeb_df.iterrows():

    with cols[i % 3]:

        name = row["Name"]
        desc = row["Description"]

        st.subheader(name)

        # ======================
        # Image Debug
        # ======================

        url = row.get("ImageURL", "")

        st.caption(f"ImageURL: {url}")

        if isinstance(url, str) and url.startswith("http"):

            try:

                response = requests.get(url)

                st.caption(f"HTTP Status: {response.status_code}")

                if response.status_code == 200:

                    img = Image.open(BytesIO(response.content))
                    st.image(img, use_container_width=True)

                else:

                    st.error("Image request failed")

            except Exception as e:

                st.error(f"Image load error: {e}")

        else:

            st.warning("Invalid Image URL")


        # ======================
        # Description
        # ======================

        st.write(desc)


        # ======================
        # Select button
        # ======================

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
