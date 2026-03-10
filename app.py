import streamlit as st

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# ======================
# CART SESSION
# ======================

if "cart" not in st.session_state:
    st.session_state.cart = []

# ======================
# STYLE
# ======================

st.markdown("""
<style>

.block-container{
padding-top:0rem;
padding-left:0rem;
padding-right:0rem;
}

.header{
position:sticky;
top:0;
z-index:999;
background:white;
padding:18px 60px;
border-bottom:1px solid #eee;
display:flex;
justify-content:space-between;
align-items:center;
font-family:Helvetica, Arial, sans-serif;
}

.logo{
font-size:28px;
font-weight:700;
letter-spacing:2px;
}

.nav{
display:flex;
gap:35px;
font-size:16px;
color:#444;
}

.hero img{
width:100%;
height:520px;
object-fit:cover;
}

.hero-title{
font-size:58px;
font-weight:700;
text-align:center;
margin-top:60px;
font-family:Helvetica, Arial, sans-serif;
}

.hero-sub{
font-size:20px;
color:#666;
text-align:center;
margin-top:10px;
}

.stButton button{
background:black;
color:white;
border:none;
height:55px;
font-size:18px;
border-radius:6px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================

st.markdown("""
<div class="header">

<div class="logo">AI STYLIST</div>

<div class="nav">
<span>Celebrity Styling</span>
<span>Collections</span>
<span>Trending</span>
<span>About</span>
</div>

</div>
""", unsafe_allow_html=True)

# ======================
# HERO
# ======================

st.markdown("""
<div class="hero">
<img src="https://images.unsplash.com/photo-1490481651871-ab68de25d43d">
</div>
""", unsafe_allow_html=True)

st.markdown(
'<div class="hero-title">AI Celebrity Styling Platform</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="hero-sub">AI powered fashion styling assistant for celebrity looks</div>',
unsafe_allow_html=True
)

st.write("")
st.write("")

# ======================
# START BUTTON
# ======================

col1, col2, col3 = st.columns([2,1,2])

with col2:
    if st.button("Start Styling"):
        st.switch_page("pages/celebrity.py")

st.write("")
st.write("")

# ======================
# INFO
# ======================

st.markdown("""
<h2 style='text-align:center;'>AI Powered Fashion Styling</h2>

<p style='text-align:center; font-size:18px; color:#666;'>
Select a celebrity, choose an event and styling preferences,
discover curated fashion pieces and generate brand request emails automatically.
</p>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ======================
# NAV BUTTONS
# ======================

col1, col2 = st.columns(2)

with col1:
    if st.button("Select Celebrity"):
        st.switch_page("pages/celebrity.py")

with col2:
    if st.button("Browse Clothing"):
        st.switch_page("pages/clothing.py")

# ======================
# SIDEBAR CART
# ======================

st.sidebar.title("🛍 Stylist Cart")

cart = st.session_state.cart

if len(cart) == 0:
    st.sidebar.write("No items saved")

for i,item in enumerate(cart):

    st.sidebar.image(item["ImageURL"], width=80)
    st.sidebar.markdown(f"**{item['Brand']}**")
    st.sidebar.caption(item["Name"])

    if st.sidebar.button("Remove", key=f"remove_sidebar_{i}"):
        st.session_state.cart.pop(i)
        st.rerun()

st.sidebar.divider()

if st.sidebar.button("Open Cart"):
    st.switch_page("pages/cart.py")

