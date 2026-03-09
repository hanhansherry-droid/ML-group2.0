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

st.subheader("Navigation")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⭐ Select Celebrity")
    st.markdown("Go to the celebrity styling page.")
    st.markdown("[Open Celebrity Page](./celebrity)")

with col2:
    st.markdown("### 👗 Browse Clothing")
    st.markdown("Explore the clothing collection.")
    st.markdown("[Open Clothing Page](./clothing)")

st.divider()

# ======================
# Clothing preview
# ======================

st.header("New Collection")

df = pd.read_excel("items.xlsx")

cols = st.columns(4)

for i, row in df.head(8).iterrows():

    with cols[i % 4]:

        try:
            st.image(row["ImagePath"])
        except:
            st.write("Image not found")

        st.write(row["Name"])

        st.caption(row["Brand"])

