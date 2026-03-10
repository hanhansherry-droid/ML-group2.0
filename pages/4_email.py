import streamlit as st
import pandas as pd
import smtplib
import os
import requests

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from collections import defaultdict

st.set_page_config(page_title="Sample Request Email", layout="wide")

st.title("Sample Request Email")

# ======================
# PATH
# ======================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONTACT_PATH = os.path.join(BASE_DIR, "brand_contacts.xlsx")
CELEB_PATH = os.path.join(BASE_DIR, "celebrities.xlsx")

# ======================
# Load contacts
# ======================

@st.cache_data
def load_contacts():

    if os.path.exists(CONTACT_PATH):

        df = pd.read_excel(CONTACT_PATH)
        df.columns = df.columns.str.strip()

        return df

    return pd.DataFrame(columns=["brand","contact_name","email"])

contacts = load_contacts()

# ======================
# Load celebrities
# ======================

@st.cache_data
def load_celebrities():

    if os.path.exists(CELEB_PATH):

        df = pd.read_excel(CELEB_PATH)
        df.columns = df.columns.str.strip()

        return df

    return pd.DataFrame(columns=["Name","Description","ImageURL"])

celeb_df = load_celebrities()

# ======================
# Get selected celebrity
# ======================

selected_celebrity = st.session_state.get("selected_celebrity")

if selected_celebrity is None:

    st.warning("Please select a celebrity first.")

    if st.button("Go to Celebrity Page"):
        st.switch_page("pages/1_celebrity.py")

    st.stop()

row = celeb_df[celeb_df["Name"] == selected_celebrity].iloc[0]

artist_name = row["Name"]
artist_intro = row["Description"]

# ======================
# Celebrity info
# ======================

st.subheader("Celebrity")

col1, col2 = st.columns([1,2])

with col1:

    if "ImageURL" in row and str(row["ImageURL"]).startswith("http"):
        st.image(row["ImageURL"], use_container_width=True)

with col2:

    st.write(artist_name)
    st.write(artist_intro)

# ======================
# Get cart items
# ======================

items = st.session_state.get("email_items", [])

if len(items) == 0:

    st.warning("No clothing selected")

    if st.button("Go to Clothing"):
        st.switch_page("pages/2_clothing.py")

    st.stop()

# ======================
# Show selected looks
# ======================

st.subheader("Selected Looks")

for item in items:

    col1, col2 = st.columns([1,2])

    with col1:
        st.image(item["ImageURL"], width=200)

    with col2:
        st.write(item["Brand"])
        st.write(item["Name"])

# ======================
# Group by brand
# ======================

brand_groups = defaultdict(list)

for item in items:
    brand_groups[item["Brand"]].append(item)

# ======================
# Event inputs
# ======================

st.divider()

studio_name = st.text_input("Studio Name")
event_name = st.text_input("Event Name")
event_intro = st.text_area("Event Introduction")

# ======================
# Gmail send
# ======================

def send_email(to_email, subject, html, brand_items):

    sender = st.secrets["email"]["sender"]
    password = st.secrets["email"]["password"]

    msg = MIMEMultipart("related")

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    msg_alt = MIMEMultipart("alternative")
    msg.attach(msg_alt)

    msg_alt.attach(MIMEText(html, "html"))

    for i,item in enumerate(brand_items):

        response = requests.get(item["ImageURL"], timeout=10)

        if response.status_code != 200:
            continue

        img_data = response.content

        image = MIMEImage(img_data)

        cid = f"look{i}"

        image.add_header("Content-ID", f"<{cid}>")

        msg.attach(image)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.sendmail(sender, to_email, msg.as_string())

# ======================
# Generate emails
# ======================

st.divider()

sent_brands = []

if st.button("Generate Emails"):

    for brand, brand_items in brand_groups.items():

        brand_row = contacts[contacts["brand"] == brand]

        if len(brand_row) == 0:
            st.warning(f"No contact info for {brand}")
            continue

        contact_name = brand_row.iloc[0]["contact_name"]
        contact_email = brand_row.iloc[0]["email"]

        looks_html = ""

        for i,item in enumerate(brand_items):

            looks_html += f"""
            <p><b>{item['Brand']} {item['Name']}</b></p>
            <img src="cid:look{i}" width="300"><br><br>
            """

        html = f"""
<p>Dear {contact_name},</p>

<p>This is stylist {studio_name}.</p>

<p>I’m requesting samples for <b>{artist_name}</b> for <b>{event_name}</b>.</p>

<p>{event_intro}</p>

<p><b>Artist Introduction</b></p>

<p>{artist_intro}</p>

<p><b>Selected Looks</b></p>

{looks_html}

<p>Best regards,<br>
{studio_name}</p>
"""

        st.markdown(f"### Email Preview — {brand}")

        preview_html = ""

        for item in brand_items:

            preview_html += f"""
            <p><b>{item['Brand']} {item['Name']}</b></p>
            <img src="{item['ImageURL']}" width="300"><br><br>
            """

        preview_email = f"""
<p>Dear {contact_name},</p>

<p>This is stylist {studio_name}.</p>

<p>I’m requesting samples for <b>{artist_name}</b> for <b>{event_name}</b>.</p>

<p>{event_intro}</p>

<p><b>Artist Introduction</b></p>

<p>{artist_intro}</p>

<p><b>Selected Looks</b></p>

{preview_html}

<p>Best regards,<br>
{studio_name}</p>
"""

        st.markdown(preview_email, unsafe_allow_html=True)

        if st.button(f"Send Email to {brand}", key=f"send_{brand}"):

            send_email(
                contact_email,
                f"Sample Request – {artist_name}",
                html,
                brand_items
            )

            sent_brands.append(brand)

# ======================
# Sample Board
# ======================

st.divider()

st.subheader("Sample Selection Board")

cols = st.columns(4)

for i,item in enumerate(items):

    with cols[i%4]:

        st.image(item["ImageURL"], use_container_width=True)

        st.markdown(f"**{item['Brand']}**")
        st.caption(item["Name"])

# ======================
# Send Success Message
# ======================

if len(sent_brands) > 0:

    st.divider()

    st.success(
        "Emails successfully sent to: " + ", ".join(sent_brands)
    )

# ======================
# Back Button
# ======================

st.divider()

if st.button("Back to Cart"):

    st.switch_page("pages/3_cart.py")
