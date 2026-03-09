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

/* Main title */

.main-title {
    font-size: 56px;
    font-weight: 700;
    text-align: center;
}

/* subtitle */

.subtitle {
    text-align: center;
    font-size: 22px;
    color: #555;
}

/* section title */

.section-title{
    font-size:32px;
    font-weight:600;
    text-align:center;
    margin-top:40px;
}

/* step card */

.step-card{
    background:white;
    padding:25px;
    border-radius:12px;
    text-align:center;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
}

/* buttons */

.stButton button{
    height:60px;
    font-size:20px;
    border-radius:10px;
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

st.markdown('<p class="main-title">AI Celebrity Styling Platform</p>', unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">AI powered styling assistant for celebrity fashion selection</p>',
    unsafe_allow_html=True
)

st.write("")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    if st.button("⭐ Start Styling", use_container_width=True):
        st.switch_page("pages/celebrity.py")

st.write("")

st.image(
    "https://images.unsplash.com/photo-1529139574466-a303027c1d8b",
    use_container_width=True
)

# ======================
# HOW IT WORKS
# ======================

st.markdown('<p class="section-title">How the Platform Works</p>', unsafe_allow_html=True)

st.write("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="step-card">
    <h3>1</h3>
    <b>Select Celebrity</b>
    <p>Choose the celebrity you are styling.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
    <h3>2</h3>
    <b>Define Event</b>
    <p>Select occasion and rental date.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
    <h3>3</h3>
    <b>Browse Clothing</b>
    <p>Explore AI-recommended fashion pieces.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="step-card">
    <h3>4</h3>
    <b>Generate Email</b>
    <p>Create brand sample request emails.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ======================
# CTA Buttons
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
