import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict

st.set_page_config(page_title="Sample Request Email")

st.title("Fashion Sample Request Email")

# =========================
# Load brand contacts
# =========================

@st.cache_data
def load_contacts():
    return pd.read_excel("brand_contacts.xlsx")

contacts = load_contacts()

# =========================
# Load celebrity database
# =========================

@st.cache_data
def load_celebrities():
    return pd.read_excel("celebrities.xlsx")

celeb_df = load_celebrities()

# =========================
# Get selected celebrity
# =========================

selected_celebrity = st.session_state.get("selected_celebrity")

if selected_celebrity is None:
    st.warning("No celebrity selected")
    st.stop()

celeb_row = celeb_df[celeb_df["Name"] == selected_celebrity].iloc[0]

artist_name = celeb_row["Name"]
artist_intro = celeb_row["Description"]

# =========================
# Celebrity display
# =========================

st.subheader("Celebrity")

st.write("Artist:", artist_name)

st.write(artist_intro)

# 预留明星图片接口
# 你以后可以加：

# st.image(celeb_row["ImageURL"])

# =========================
# Get cart items
# =========================

items = st.session_state.get("email_items", [])

if len(items) == 0:
    st.warning("No clothing selected")
    st.stop()

# =========================
# Show selected looks
# =========================

st.subheader("Selected Looks")

for item in items:

    col1,col2 = st.columns([1,2])

    with col1:
        st.image(item["ImageURL"], width=200)

    with col2:
        st.write(item["Brand"])
        st.write(item["Name"])

# =========================
# Group items by brand
# =========================

brand_groups = defaultdict(list)

for item in items:
    brand_groups[item["Brand"]].append(item)

# =========================
# Event inputs
# =========================

st.divider()

st.header("Styling Request Information")

studio_name = st.text_input("Studio Name")

event_name = st.text_input("Program / Event Name")

event_intro = st.text_area("Event Introduction")

usage_context = st.text_area("Usage Context")

# =========================
# Gmail send function
# =========================

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

        server.sendmail(
            sender,
            to_email,
            msg.as_string()
        )

# =========================
# Generate emails
# =========================

if st.button("Generate Emails"):

    st.session_state.generated_emails = {}

    for brand, brand_items in brand_groups.items():

        brand_row = contacts[contacts["brand"] == brand]

        if len(brand_row) == 0:
            continue

        contact_name = brand_row.iloc[0]["contact_name"]
        contact_email = brand_row.iloc[0]["email"]

        looks_html = ""

        for item in brand_items:

            looks_html += f"""
            <p><b>{item['Brand']} {item['Name']}</b></p>
            <img src="{item['ImageURL']}" width="300"><br><br>
            """

        html = f"""
<p>Dear {contact_name},</p>

<p>Hope you’re doing well!</p>

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

        st.session_state.generated_emails[brand] = {
            "email": contact_email,
            "contact": contact_name,
            "html": html
        }

# =========================
# Display generated emails
# =========================

if "generated_emails" in st.session_state:

    st.divider()

    for brand,data in st.session_state.generated_emails.items():

        st.subheader(f"{brand}")

        st.write("To:", data["email"])

        st.markdown(data["html"], unsafe_allow_html=True)

        if st.button(f"Send Email to {brand}"):

            send_email(
                data["email"],
                f"Sample Request – {artist_name}",
                data["html"]
            )

            st.success(f"Email sent to {brand}")
