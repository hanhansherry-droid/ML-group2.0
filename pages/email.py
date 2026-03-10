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
# Get cart items
# =========================

items = st.session_state.get("email_items", [])

if len(items) == 0:
    st.warning("No items selected")
    st.stop()

# =========================
# Group items by brand
# =========================

brand_groups = defaultdict(list)

for item in items:
    brand_groups[item["Brand"]].append(item)

# =========================
# Artist info
# =========================

artist_name = "Sdanny Lee"

artist_intro = """
Sdanny Lee is a singer and performer known for her powerful stage presence
and distinctive modern aesthetic. She has collaborated with several
fashion houses and appeared in high-profile cultural events.
"""

# =========================
# Event Inputs
# =========================

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
# Generate Emails
# =========================

if st.button("Generate Emails"):

    st.session_state.generated_emails = {}

    for brand, items in brand_groups.items():

        brand_row = contacts[contacts["brand"] == brand]

        if len(brand_row) == 0:
            continue

        contact_name = brand_row.iloc[0]["contact_name"]
        contact_email = brand_row.iloc[0]["email"]

        looks_html = ""

        for item in items:

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
# Display Generated Emails
# =========================

if "generated_emails" in st.session_state:

    st.divider()

    for brand, data in st.session_state.generated_emails.items():

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
