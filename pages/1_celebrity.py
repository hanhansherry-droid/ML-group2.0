import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Select Celebrity", layout="wide")

st.title("AI Fashion Stylist")
st.subheader("Select Celebrity")


# PATH


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELEB_PATH = os.path.join(BASE_DIR, "celebrities.xlsx")


# Load data


@st.cache_data
def load_celebrities():

    df = pd.read_excel(CELEB_PATH)
    df.columns = df.columns.str.strip()

    # 修复URL读取问题
    df["ImageURL"] = df["ImageURL"].astype(str).str.strip()

    return df

celeb_df = load_celebrities()


# Selector


celebrity_list = celeb_df["Name"].dropna().tolist()

selected_name = st.selectbox(
    "Choose a celebrity",
    celebrity_list
)


# Display info


row = celeb_df[celeb_df["Name"] == selected_name].iloc[0]

st.divider()

col1, col2 = st.columns([1,1])


# Image


with col1:

    image_url = row["ImageURL"]

    if isinstance(image_url, str) and image_url.startswith("http"):
        st.image(image_url, use_container_width=True)
    else:
        st.warning("Image not available")


# Info

with col2:

    st.subheader(row["Name"])

    st.write("Profession:", row["Profession"])
    st.write("Nationality:", row["Nationality"])

    st.write("Style Tags")
    st.caption(row["Style Tags"])

    st.write("Description")
    st.write(row["Description"])


# Save Celebrity


st.divider()

if st.button("Save Celebrity", key="save_celeb"):

    st.session_state.selected_celebrity = selected_name

    st.success(f"{selected_name} saved for styling")

# Continue workflow


if "selected_celebrity" in st.session_state:

    st.write("Current styling target:", st.session_state.selected_celebrity)

    if st.button("Continue to Clothing", key="continue_clothing"):

        st.switch_page("pages/2_clothing.py")

