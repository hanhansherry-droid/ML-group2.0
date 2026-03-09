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

/* remove default padding */

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
font-size:26px;
font-weight:700;
letter-spacing:3px;
}

/* nav menu */

.nav{
display:flex;
gap:35px;
font-size:16px;
color:#444;
}

/* ===== HERO SECTION ===== */

.hero{
position:relative;
width:100%;
height:540px;
overflow:hidden;
}

.hero img{
width:100%;
height:540px;
object-fit:cover;
}

/* hero text */

.hero-text{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
color:white;
text-align:center;
font-family:Helvetica, Arial, sans-serif;
}

.hero-text h1{
font-size:64px;
font-weight:700;
letter-spacing:1px;
}

.hero-text p{
font-size:22px;
margin-top:10px;
}

/* CTA button */

.stButton button{
background:black;
color:white;
border:none;
height:55px;
font-size:18px;
border-radius:6px;
}

/* section */

.section{
padding:80px 20%;
text-align:center;
font-family:Helvetica, Arial, sans-serif;
}

</style>
""", unsafe_allow_html=True)

# ======================
# HEADER (像官网导航)
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
<div class="hero">

<img src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f">

<div class="hero-text">
<h1>AI Celebrity Styling Platform</h1>
<p>AI powered fashion styling assistant</p>
</div>

</div>
""", unsafe_allow_html=True)

# ======================
# CTA BUTTON
# ======================

col1, col2, col3 = st.columns([2,1,2])

with col2:
    if st.button("Start Styling"):
        st.switch_page("pages/celebrity.py")

# ======================
# INFO SECTION
# ======================

st.markdown("""
<div class="section">

<h2>AI Powered Fashion Styling</h2>

<p>
Select a celebrity, choose an event and styling preferences,
discover curated fashion pieces and generate brand request emails automatically.
</p>

</div>
""", unsafe_allow_html=True)

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
