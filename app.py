import streamlit as st

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# ======================
# GLOBAL STYLE
# ======================

st.markdown("""
<style>

/* remove padding */

.block-container{
padding-top:0rem;
padding-left:0rem;
padding-right:0rem;
}

/* ===== HEADER ===== */

.header{
position:sticky;
top:0;
z-index:999;
background:white;
padding:20px 60px;
border-bottom:1px solid #eee;
display:flex;
justify-content:space-between;
align-items:center;
font-family:Helvetica, Arial, sans-serif;
}

/* logo */

.logo{
font-size:28px;
font-weight:700;
letter-spacing:2px;
}

/* nav */

.nav{
display:flex;
gap:35px;
font-size:16px;
color:#444;
}

/* ===== HERO IMAGE ===== */

.hero-img img{
width:100%;
height:520px;
object-fit:cover;
}

/* hero title */

.hero-title{
font-size:56px;
font-weight:700;
text-align:center;
margin-top:60px;
}

/* hero subtitle */

.hero-sub{
font-size:20px;
color:#666;
text-align:center;
margin-top:10px;
}

/* buttons */

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
# HERO IMAGE
# ======================

st.markdown("""
<div class="hero-img">
<img src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f">
</div>
""", unsafe_allow_html=True)

# ======================
# HERO TEXT
# ======================

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
# MAIN BUTTON
# ======================

col1, col2, col3 = st.columns([2,1,2])

with col2:
    if st.button("Start Styling"):
        st.switch_page("pages/celebrity.py")

st.write("")
st.write("")

# ======================
# SECOND SECTION
# ======================

st.markdown(
"""
<h2 style='text-align:center;'>AI Powered Fashion Styling</h2>
<p style='text-align:center; font-size:18px; color:#666;'>
Select a celebrity, choose an event and styling preferences,
discover curated fashion pieces and generate brand request emails automatically.
</p>
""",
unsafe_allow_html=True
)

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

with col2:
    if st.button("Browse Clothing"):
        st.switch_page("pages/clothing.py")

