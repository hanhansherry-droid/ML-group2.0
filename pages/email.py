import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Fashion Sample Request")

st.title("Sample Request Email")

# =========================
# Load contacts
# =========================

@st.cache_data
def load_contacts():
    return pd.read_excel("brand_contacts.xlsx")

contacts = load_contacts()

# =========================
# Get cart items
# =========================

items = st.session_state.get("email_items", [])

if len(items) == 0:

    st.warning("No items selected")

    st.stop()

# =========================
# Detect brand
# =========================

brand = items[0]["Brand"]

brand_row = contacts[contacts["brand"] == brand].iloc[0]

recipient_name = brand_row["contact_name"]
recipient_email = brand_row["email"]

st.subheader("Brand Contact")

st.write("Brand:", brand)
st.write("Contact:", recipient_name)
st.write("Email:", recipient_email)

# =========================
# Artist info
# =========================

artist_name = "Sdanny Lee"

artist_intro = """
Sdanny Lee is a singer and performer known for her powerful stage presence and modern aesthetic.
"""

st.divider()

# =========================
# Event Inputs
# =========================

studio_name = st.text_input("Studio Name")

event_name = st.text_input("Program / Event")

event_intro = st.text_area("Event Introduction")

usage_context = st.text_area("Usage Context")

# =========================
# Generate email
# =========================

if st.button("Generate Email"):

    looks_html = ""

    for item in items:

        looks_html += f"""
        <p><b>{item['Brand']} {item['Name']}</b></p>
        <img src="{item['ImageURL']}" width="300"><br><br>
        """

    preview_html = f"""
<p>Dear {recipient_name},</p>

<p>Hope you're doing well.</p>

<p>This is stylist Huna from <b>{studio_name}</b>.</p>

<p>I’m reaching out regarding a sample request for <b>{artist_name}</b>, who will participate in <b>{event_name}</b>.</p>

<p>{event_intro}</p>

<p><b>Artist Introduction</b></p>

<p>{artist_intro}</p>

<p>{usage_context}</p>

<p><b>Selected Looks</b></p>

{looks_html}

<p>Kind regards,<br>
Huna<br>
{studio_name}</p>
"""

    st.session_state.email_preview = preview_html

# =========================
# Preview
# =========================

if "email_preview" in st.session_state:

    st.divider()

    st.subheader("Email Preview")

    st.markdown(st.session_state.email_preview, unsafe_allow_html=True)
