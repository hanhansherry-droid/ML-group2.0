import streamlit as st
import pandas as pd
from collections import defaultdict
from openai import OpenAI

st.title("🛍 Saved Looks")

cart = st.session_state.get("cart", [])

if len(cart) == 0:
    st.info("No items saved yet.")

else:

    for i,item in enumerate(cart):

        col1,col2 = st.columns([1,2])

        with col1:
            st.image(item["ImageURL"], use_container_width=True)

        with col2:

            st.markdown(f"**{item['Brand']}**")
            st.write(item["Name"])

            st.write("Note:", item["note"])

            if st.button("Remove", key=f"remove_{i}"):

                st.session_state.cart.pop(i)
                st.rerun()

# ==============================
# EMAIL GENERATION
# ==============================

st.divider()
st.subheader("Generate Brand Emails")

CONTACT_PATH = "brand_contacts.xlsx"

@st.cache_data
def load_contacts():
    return pd.read_excel(CONTACT_PATH)

contacts = load_contacts()

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

artist_info = {
"name":"Sdanny Lee",
"description":"Singer and performer known for modern stage aesthetic"
}

def get_brand_email(brand):

    row = contacts[contacts["brand"]==brand]

    if len(row)>0:
        return row.iloc[0]["email"]

    return None

def generate_email(brand,items):

    looks = "\n".join([f"- {i['Brand']} {i['Name']}" for i in items])

    prompt = f"""
Write a professional fashion sample request email.

Artist: {artist_info['name']}

Artist description:
{artist_info['description']}

Brand:
{brand}

Requested items:
{looks}

Tone: professional stylist.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content

brand_groups = defaultdict(list)

for item in cart:
    brand_groups[item["Brand"]].append(item)

if st.button("Generate Emails"):

    for brand,items in brand_groups.items():

        email = get_brand_email(brand)

        st.markdown(f"### {brand}")
        st.write("Email:",email)

        email_text = generate_email(brand,items)

        st.text_area(
            f"Email for {brand}",
            email_text,
            height=250
        )
