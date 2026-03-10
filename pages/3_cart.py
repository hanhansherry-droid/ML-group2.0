import streamlit as st
import pandas as pd
import os
from collections import defaultdict

st.set_page_config(page_title="Saved Looks", layout="wide")

st.title("🛍 Saved Looks")

# ==============================
# PATH
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTACT_PATH = os.path.join(BASE_DIR, "brand_contacts.xlsx")

# ==============================
# LOAD BRAND CONTACTS
# ==============================

def load_contacts():

    df = pd.read_excel(CONTACT_PATH)

    df.columns = df.columns.str.strip()

    if "brand" in df.columns:
        df["brand"] = df["brand"].astype(str).str.strip()

    return df

contacts = load_contacts()

# ==============================
# CART DATA
# ==============================

cart = st.session_state.get("cart", [])

if len(cart) == 0:

    st.info("No items saved yet.")

else:

    st.subheader("Selected Looks")

    for i, item in enumerate(cart):

        col1, col2 = st.columns([1,2])

        with col1:
            st.image(item["ImageURL"], use_container_width=True)

        with col2:

            st.markdown(f"**{item['Brand']}**")

            st.write(item["Name"])

            note = item.get("note","")

            st.write("Note:", note)

            if st.button("Remove", key=f"remove_cart_{i}"):

                st.session_state.cart.pop(i)

                st.rerun()

# ==============================
# GROUP ITEMS BY BRAND
# ==============================

brand_groups = defaultdict(list)

for item in cart:

    brand_groups[item["Brand"]].append(item)

# ==============================
# BRAND CONTACTS
# ==============================

st.divider()

st.subheader("Brand Contacts")

if len(cart) > 0:

    for brand, items in brand_groups.items():

        st.markdown(f"### {brand}")

        row = contacts[
            contacts["brand"].str.strip().str.lower()
            ==
            brand.strip().lower()
        ]

        if len(row) > 0:

            contact = row.iloc[0]["contact_name"]
            email = row.iloc[0]["email"]

            st.write("Contact:", contact)

            st.write("Email:", email)

        else:

            st.warning("No contact information found for this brand.")

# ==============================
# REQUEST SAMPLE
# ==============================

st.divider()

if len(cart) > 0:

    if st.button("Request Samples", key="request_samples_btn"):

        # send cart items to email page
        st.session_state.email_items = st.session_state.cart

        st.switch_page("pages/4_email.py")
