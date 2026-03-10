import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict

st.title("Sample Request Email")

# ======================
# Load contacts
# ======================

@st.cache_data
def load_contacts():
    return pd.read_excel("brand_contacts.xlsx")

contacts = load_contacts()

# ======================
# Load celebrities
# ======================

@st.cache_data
def load_celebrities():
    return pd.read_excel("celebrities.xlsx")

celeb_df = load_celebrities()

# ======================
# Get selected celebrity
# ======================

selected_celebrity = st.session_state.get("selected_celebrity")

row = celeb_df[celeb_df["Name"] == selected_celebrity].iloc[0]

artist_name = row["Name"]
artist_intro = row["Description"]

st.subheader("Celebrity")

st.write(artist_name)
st.write(artist_intro)

# 预留明星图片
# st.image(row["ImageURL"])

# ======================
# Get cart items
# ======================

items = st.session_state.get("email_items", [])

if len(items) == 0:
    st.warning("No clothing selected")
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

studio_name = st.text_input("Studio Name")
event_name = st.text_input("Event Name")
event_intro = st.text_area("Event Introduction")

# ======================
# Gmail send
# ======================

def send_email(to_email, subject, html):

    sender = st.secrets["email"]["sender"]
    password = st.secrets["email"]["password"]

    msg = MIMEMultipart("alternative")

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.sendmail(sender, to_email, msg.as_string())

# ======================
# Generate emails
# ======================

if st.button("Generate Emails"):

    for brand, brand_items in brand_groups.items():

        brand_row = contacts[contacts["brand"] == brand].iloc[0]

        contact_name = brand_row["contact_name"]
        contact_email = brand_row["email"]

        looks_html = ""

        for item in brand_items:

            looks_html += f"""
            <p><b>{item['Brand']} {item['Name']}</b></p>
            <img src="{item['ImageURL']}" width="300"><br><br>
            """

        html = f"""
<p>Dear {contact_name},</p>

<p>This is stylist Huna.</p>

<p>I’m requesting samples for <b>{artist_name}</b> for <b>{event_name}</b>.</p>

<p>{event_intro}</p>

<p><b>Artist Introduction</b></p>

<p>{artist_intro}</p>

<p><b>Selected Looks</b></p>

{looks_html}

<p>Best regards,<br>
Huna</p>
"""

        st.markdown(html, unsafe_allow_html=True)

        if st.button(f"Send Email to {brand}"):

            send_email(
                contact_email,
                f"Sample Request – {artist_name}",
                html
            )

            st.success("Email sent!")
