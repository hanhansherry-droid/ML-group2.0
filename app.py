import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# =========================
# CSS UI 美化
# =========================

st.markdown("""
<style>

.main-title{
font-size:55px;
font-weight:700;
text-align:center;
margin-top:20px;
}

.subtitle{
text-align:center;
font-size:20px;
color:gray;
}

.navbar{
font-size:18px;
}

.product-card{
padding:10px;
text-align:center;
}

.product-name{
font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Navbar
# =========================

nav1, nav2, nav3 = st.columns([1,4,1])

with nav1:
    st.write("☰ Menu")

with nav2:
    st.markdown(
        "<h1 style='text-align:center'>AI STYLING</h1>",
        unsafe_allow_html=True
    )

with nav3:
    st.write("❤ Wishlist")

st.divider()

# =========================
# Banner
# =========================

st.image(
    "https://images.unsplash.com/photo-1490481651871-ab68de25d43d",
    use_container_width=True
)

st.markdown(
    "<div class='main-title'>AI Celebrity Styling Platform</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Discover fashion pieces for celebrity styling</div>",
    unsafe_allow_html=True
)

st.write("")

# =========================
# Navigation Buttons
# =========================

b1, b2 = st.columns(2)

with b1:
    st.page_link("pages/Celebrity.py", label="⭐ Select Celebrity")

with b2:
    st.page_link("pages/Clothing.py", label="👗 Browse Clothing")

st.write("")
st.write("")

# =========================
# Clothing Grid
# =========================

st.header("New Collection")

df = pd.read_excel("items.xlsx")

cols = st.columns(4)

for i,row in df.head(8).iterrows():

    with cols[i % 4]:

        st.image(row["ImagePath"])

        st.markdown(
            f"<div class='product-name'>{row['Name']}</div>",
            unsafe_allow_html=True
        )

        st.caption(row["Brand"])
