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
padding-left:0rem;
padding-right:0rem;
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

.nav{
display:flex;
gap:35px;
font-size:16px;
color:#444;
}

/* HERO */

.hero img{
width:100%;
height:520px;
object-fit:cover;
}

/* TITLE */

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

/* BUTTON */

.stButton button{
background:black;
color:white;
border:none;
height:55px;
font-size:18px;
border-radius:6px;
transition:0.3s;
}

.stButton button:hover{
background:#333;
}

/* FEATURE */

.feature{
text-align:center;
margin-top:40px;
}

.feature h2{
font-size:32px;
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

/* IMAGE STYLE */

img{
border-radius:10px;
}

img:hover{
transform:scale(1.02);
transition:0.3s;
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
    if st.button("Start Styling", key="start_styling"):
        st.switch_page("pages/1_celebrity.py")

st.write("")
st.write("")

# ======================
# WORKFLOW STEPS
# ======================

st.markdown("""
<div class="feature">

<h2>How It Works</h2>

<p>
1. Select a celebrity style reference  
2. Explore curated fashion pieces  
3. Save looks to your stylist cart  
4. Generate brand sample request emails
</p>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ======================
# NAV BUTTONS
# ======================

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Select Celebrity", key="btn_celebrity"):
        st.switch_page("pages/1_celebrity.py")

with col2:
    if st.button("Browse Clothing", key="btn_clothing"):
        st.switch_page("pages/2_clothing.py")

with col3:
    if st.button("Generate Email", key="btn_email"):
        st.switch_page("pages/4_email.py")

st.write("")
st.write("")

# ======================
# TRENDING PREVIEW
# ======================

st.markdown("### Trending Looks")

col1, col2, col3, col4 = st.columns(4)

sample_images = [
"https://images.unsplash.com/photo-1520975916090-3105956dac38",
"https://images.unsplash.com/photo-1519741497674-611481863552",
"https://images.unsplash.com/photo-1503342217505-b0a15ec3261c",
"https://images.unsplash.com/photo-1529139574466-a303027c1d8b"
]

for i,col in enumerate([col1,col2,col3,col4]):
    with col:
        st.image(sample_images[i], use_container_width=True)

st.write("")
st.write("")

# ======================
# SIDEBAR WORKFLOW
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

for i, item in enumerate(cart):

    st.sidebar.image(item["ImageURL"], width=80)
    st.sidebar.markdown(f"**{item['Brand']}**")
    st.sidebar.caption(item["Name"])

    if st.sidebar.button("Remove", key=f"remove_sidebar_{i}"):
        st.session_state.cart.pop(i)
        st.rerun()

st.sidebar.divider()

if st.sidebar.button("Open Cart", key="sidebar_open_cart"):
    st.switch_page("pages/3_cart.py")
if st.sidebar.button("Open Cart", key="sidebar_open_cart"):
    st.switch_page("pages/cart.py")


