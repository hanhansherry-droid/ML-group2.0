import streamlit as st

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# ======================
# Style
# ======================

st.markdown("""
<style>

.stApp {
    background-color: #f7f7f7;
}

/* Hero title */

.hero-title{
font-size:64px;
font-weight:800;
}

/* subtitle */

.hero-sub{
font-size:22px;
color:#555;
}

/* step cards */

.step{
background:white;
padding:25px;
border-radius:12px;
text-align:center;
box-shadow:0 3px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ======================
# Sidebar
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
# HERO SECTION
# ======================

left, right = st.columns([1.2,1])

with left:

    st.markdown(
        '<div class="hero-title">AI Celebrity Styling Platform</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-sub">AI-powered fashion assistant for celebrity styling</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    if st.button("⭐ Start Styling", use_container_width=True):
        st.switch_page("pages/celebrity.py")

with right:

    st.image(
        "https://images.unsplash.com/photo-1529139574466-a303027c1d8b",
        use_container_width=True
    )

st.write("")
st.write("")
st.divider()

# ======================
# HOW IT WORKS
# ======================

st.subheader("How the Platform Works")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="step">
    <h3>1</h3>
    Select Celebrity
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="step">
    <h3>2</h3>
    Choose Event
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="step">
    <h3>3</h3>
    Browse Clothing
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="step">
    <h3>4</h3>
    Generate Email
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")
st.divider()

# ======================
# CTA SECTION
# ======================

col1, col2 = st.columns(2)

with col1:
    if st.button("⭐ Select Celebrity", use_container_width=True):
        st.switch_page("pages/celebrity.py")

with col2:
    if st.button("👗 Browse Clothing", use_container_width=True):
        st.switch_page("pages/clothing.py")

st.write("")
st.info("Use AI to explore celebrity styling and discover fashion collections.")

st.write("")
st.info("Use AI to explore celebrity styling and discover fashion collections.")

