import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ======================
# TITLE
# ======================

st.markdown(
"""
<h1 style='text-align:center;'>Select Celebrity</h1>
<p style='text-align:center; color:#666; font-size:18px;'>
Choose the celebrity you are styling for
</p>
""",
unsafe_allow_html=True
)

st.write("")
st.write("")

# ======================
# LOAD DATA
# ======================

df = pd.read_excel("celebrities.xlsx")

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "")

# ======================
# CELEBRITY SELECT
# ======================

names = df["Name"].tolist()

col1, col2, col3 = st.columns([1,2,1])

with col2:
    selected = st.selectbox("Choose Celebrity", names)

celeb = df[df["Name"] == selected].iloc[0]

st.write("")
st.write("")

# ======================
# CELEBRITY CARD
# ======================

col1, col2 = st.columns([1,2])

with col1:

    image_path = f"images/{selected}.jpg"

    try:
        st.image(image_path, use_container_width=True)
    except:
        st.write("Image not available")

with col2:

    st.markdown(
        f"""
        <h2>{celeb["Name"]}</h2>
        """,
        unsafe_allow_html=True
    )

    st.write(f"**Nationality:** {celeb['Nationality']}")
    st.write(f"**Profession:** {celeb['Profession']}")

    st.write("")
    st.write(celeb["Description"])

    st.write("")
    st.write("**Style Tags**")

    tags = celeb["StyleTags"].split(",")

    for tag in tags:
        st.markdown(
            f"<span style='background:#f2f2f2; padding:6px 12px; margin-right:8px; border-radius:12px;'>{tag.strip()}</span>",
            unsafe_allow_html=True
        )

st.write("")
st.write("")

# ======================
# NEXT BUTTON
# ======================

col1, col2, col3 = st.columns([2,1,2])

with col2:
    if st.button("Continue to Styling"):
        st.session_state["celebrity"] = selected
        st.switch_page("pages/styling.py")
