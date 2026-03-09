import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# ======================
# Title
# ======================

st.title("AI Celebrity Styling Platform")

st.write("Discover fashion pieces for celebrity styling.")

st.divider()

# ======================
# Navigation
# ======================

col1, col2 = st.columns(2)

with col1:
    st.page_link(
        "pages/1_Celebrity.py",
        label="⭐ Select Celebrity"
    )

with col2:
    st.page_link(
        "pages/Select_Clothing.py",
        label="👗 Browse Clothing"
    )

st.divider()

# ======================
# Clothing preview
# ======================

st.header("New Collection")

df = pd.read_excel("items.xlsx")

cols = st.columns(4)

for i, row in df.head(8).iterrows():

    with cols[i % 4]:

        st.image(row["ImagePath"])

        st.write(row["Name"])

        st.caption(row["Brand"])
