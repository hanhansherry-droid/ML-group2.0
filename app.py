import streamlit as st

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# ======================
# SESSION
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
max-width:1400px;
margin:auto;
}

/* HEADER */

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

/* HERO */

.hero{
position:relative;
margin-top:20px;
}

.hero img{
width:100%;
height:560px;
object-fit:cover;
border-radius:12px;
filter:brightness(60%);
}

/* HERO TEXT */

.hero-text{
position:absolute;
top:50%;
left:50%;
transform:translate(-50%,-50%);
text-align:center;
color:white;
width:100%;
}

.hero-title{
font-size:64px;
font-weight:700;
letter-spacing:1px;
text-shadow:0px 4px 40px rgba(0,0,0,0.9);
}

.hero-sub{
font-size:22px;
margin-top:15px;
text-shadow:0px 4px 20px rgba(0,0,0,0.8);
}

/* BUTTON */

.stButton button{
background:black;
color:white;
border:none;
height:60px;
font-size:20px;
border-radius:8px;
padding:0 30px;
transition:0.3s;
}

.stButton button:hover{
background:#222;
transform:scale(1.03);
}

/* FEATURE */

.feature{
text-align:center;
margin-top:70px;
}

.feature h2{
font-size:36px;
}

.feature p{
font-size:18px;
color:#666;
max-width:800px;
margin:auto;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
background:#fafafa;
border-right:1px solid #eee;
}

img{
border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================

st.markdown("""
<div class="header">

<div class="logo">AI STYLIST</div>

</div>
""", unsafe_allow_html=True)

# ======================
# HERO
# ======================

st.markdown("""
<div class="hero">

<img src="https://images.unsplash.com/photo-1544441893-675973e31985">

<div class="hero-text">

<div class="hero-title">
AI Celebrity Styling Platform
</div>

<div class="hero-sub">
AI powered fashion styling assistant for luxury celebrity looks
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ======================
# START BUTTON
# ======================

col1,col2,col3 = st.columns([2,1,2])

with col2:
    if st.button("✨ Start Styling", key="start_style"):
        st.switch_page("pages/1_celebrity.py")

st.write("")
st.write("")

# ======================
# FEATURE
# ======================

st.markdown("""
<div class="feature">

<h2>AI Powered Fashion Styling</h2>

<p>
Select a celebrity, explore curated fashion pieces,
save looks to your stylist cart and generate
brand sample request emails automatically.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ======================
# NAV BUTTONS
# ======================

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("Select Celebrity", key="nav1"):
        st.switch_page("pages/1_celebrity.py")

with col2:
    if st.button("Browse Clothing", key="nav2"):
        st.switch_page("pages/2_clothing.py")

with col3:
    if st.button("Generate Email", key="nav3"):
        st.switch_page("pages/4_email.py")

st.write("")
st.write("")

# ======================
# TRENDING
# ======================

st.markdown("### Trending Luxury Looks")

col1,col2,col3,col4 = st.columns(4)

images = [
"https://images.unsplash.com/photo-1515886657613-9f3515b0c78f",
"https://images.unsplash.com/photo-1529139574466-a303027c1d8b",
"https://images.unsplash.com/photo-1544441893-675973e31985",
"https://images.unsplash.com/photo-1509631179647-0177331693ae"
]

for i,col in enumerate([col1,col2,col3,col4]):
    with col:
        st.image(images[i], use_container_width=True)

# ======================
# SIDEBAR
# ======================

st.sidebar.markdown("### Styling Workflow")

st.sidebar.markdown("""
1️⃣ Celebrity  
2️⃣ Clothing  
3️⃣ Cart  
4️⃣ Email
""")

st.sidebar.divider()

# ======================
# SIDEBAR CART
# ======================

st.sidebar.markdown("### 🛍 Stylist Cart")

cart = st.session_state.cart

if len(cart) == 0:
    st.sidebar.write("No items saved")

for i,item in enumerate(cart):

    st.sidebar.image(item["ImageURL"], width=80)
    st.sidebar.markdown(f"**{item['Brand']}**")
    st.sidebar.caption(item["Name"])

    if st.sidebar.button("Remove", key=f"remove_{i}"):
        st.session_state.cart.pop(i)
        st.rerun()

st.sidebar.divider()

if st.sidebar.button("Open Cart", key="open_cart_unique"):
    st.switch_page("pages/3_cart.py")
