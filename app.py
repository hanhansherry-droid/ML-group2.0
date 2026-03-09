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

.stApp{
background: linear-gradient(to bottom,#f5f5f7,#ffffff);
}

/* HERO TITLE */

.hero-title{
font-size:72px;
font-weight:800;
letter-spacing:-1px;
text-align:center;
}

/* SUBTITLE */

.hero-sub{
font-size:24px;
color:#666;
text-align:center;
}

/* BUTTON */

.stButton button{
height:65px;
font-size:20px;
border-radius:12px;
background:#111;
color:white;
border:none;
}

.stButton button:hover{
background:#333;
}

/* STEP CARDS */

.card{
background:white;
padding:30px;
border-radius:14px;
text-align:center;
box-shadow:0 6px 20px rgba(0,0,0,0.06);
}

.card h3{
font-size:22px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# SIDEBAR
# ======================

st.sidebar.title("AI Stylist Platform")

st.sidebar.markdown("### Navigation")

if st.sidebar.button("⭐ Celebrity Styling"):
    st.switch_page("pages/celebrity.py")

if st.sidebar.button("👗 Clothing Collection"):
    st.switch_page("pages/clothing.py")

st.sidebar.markdown("---")
st.sidebar.caption("AI Fashion Styling Demo")

# ======================
# HERO
# ======================

st.write("")
st.write("")

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

center = st.columns([1,2,1])

with center[1]:
    if st.button("⭐ Start Styling", use_container_width=True):
        st.switch_page("pages/celebrity.py")

st.write("")
st.write("")

# ======================
# HERO IMAGE
# ======================

st.image(
"https://images.unsplash.com/photo-1529139574466-a303027c1d8b",
use_container_width=True
)

st.write("")
st.write("")

# ======================
# WORKFLOW
# ======================

st.subheader("Platform Workflow")

st.write("")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown("""
<div class="card">
<h3>1</h3>
<b>Select Celebrity</b>
<p>Choose the celebrity you are styling.</p>
</div>
""",unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="card">
<h3>2</h3>
<b>Select Event</b>
<p>Choose the event or appearance.</p>
</div>
""",unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="card">
<h3>3</h3>
<b>Choose Styling</b>
<p>Filter clothing by style and availability.</p>
</div>
""",unsafe_allow_html=True)

with c4:
    st.markdown("""
<div class="card">
<h3>4</h3>
<b>Generate Email</b>
<p>Automatically create brand request emails.</p>
</div>
""",unsafe_allow_html=True)

st.write("")
st.write("")

# ======================
# CTA
# ======================

col1,col2 = st.columns(2)

with col1:
    if st.button("⭐ Select Celebrity", use_container_width=True):
        st.switch_page("pages/celebrity.py")

with col2:
    if st.button("👗 Browse Clothing", use_container_width=True):
        st.switch_page("pages/clothing.py")

st.write("")
st.info("Use AI to explore celebrity styling and discover fashion collections.")
