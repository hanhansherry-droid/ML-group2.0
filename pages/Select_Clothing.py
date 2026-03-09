import streamlit as st
from utils.data_loader import load_items
from PIL import Image

st.title("Select Clothing")

items, tags = load_items()

if "cart" not in st.session_state:
    st.session_state.cart = []

# filters
brand = st.sidebar.multiselect(
    "Brand",
    items["Brand"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    items["Category"].unique()
)

color = st.sidebar.multiselect(
    "Color",
    items["Color"].unique()
)

filtered = items.copy()

if brand:
    filtered = filtered[filtered["Brand"].isin(brand)]

if category:
    filtered = filtered[filtered["Category"].isin(category)]

if color:
    filtered = filtered[filtered["Color"].isin(color)]

cols = st.columns(4)

for i, row in filtered.iterrows():

    col = cols[i % 4]

    with col:

        image = Image.open(row["ImagePath"])

        st.image(image)

        st.write(row["Name"])
        st.write(row["Brand"])

        if st.button("Add", key=row["ItemID"]):

            st.session_state.cart.append(row["ItemID"])