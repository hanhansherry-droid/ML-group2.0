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

/* sticky header */

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
}

/* logo */

.logo{
font-size:28px;
font-weight:700;
letter-spacing:2px;
}

/* hero section */

.hero{
position:relative;
width:100%;
height:520px;
overflow:hidden;
}

.hero img{
width:100%;
height:520px;
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
}

.hero-text h1{
font-size:60px;
font-weight:700;
}

.hero-text p{
font-size:22px;
margin-top:10px;
}

/* button */

.hero-btn button{
background:black;
color:white;
border:none;
height:55px;
font-size:18px;
border-radius:6px;
margin-top:20px;
}

/* section */

.section{
padding:80px 20%;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================

st.markdown("""
<div class="header">
<div class="logo">AI STYLIST</div>
<div>
Celebrity Styling &nbsp;&nbsp;&nbsp; Clothing Collection
</div>
</div>
""", unsafe_allow_html=True)

# ======================
# HERO IMAGE
# ======================

st.markdown("""
<div class="hero">
<img src="https://images.unsplash.com/photo-1544441893-675973e31985">
<div class="hero-text">
<h1>AI Celebrity Styling Platform</h1>
<p>AI powered fashion styling assistant</p>
</div>
</div>
""", unsafe_allow_html=True)

# ======================
# BUTTON
# ======================

col1,col2,col3 = st.columns([2,1,2])

with col2:
    if st.button("Start Styling"):
        st.switch_page("pages/celebrity.py")

# ======================
# SECTION
# ======================

st.markdown("""
<div class="section">

<h2>Explore AI Powered Styling</h2>

<p>
Select a celebrity, choose an event and styling preferences, 
discover curated fashion pieces and generate brand request emails automatically.
</p>

</div>
""", unsafe_allow_html=True)

# ======================
# BUTTONS
# ======================

col1,col2 = st.columns(2)

with col1:
    if st.button("Select Celebrity"):
        st.switch_page("pages/celebrity.py")

with col2:
    if st.button("Browse Clothing"):
        st.switch_page("pages/clothing.py")
