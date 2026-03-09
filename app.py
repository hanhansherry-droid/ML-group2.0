import streamlit as st

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# ======================
# Style (背景 + UI)
# ======================

st.markdown("""
<style>

.stApp {
    background-color: #f7f7f7;
}

.main-title {
    font-size: 48px;
    font-weight: 700;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: gray;
}

.nav-button button {
    height: 70px;
    font-size: 20px;
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
# Hero Section
# ======================

st.markdown('<p class="main-title">AI Celebrity Styling Platform</p>', unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">Discover fashion pieces for celebrity styling</p>',
    unsafe_allow_html=True
)

st.image(
    "https://images.unsplash.com/photo-1529139574466-a303027c1d8b",
    use_container_width=True
)

st.write("")

# ======================
# Navigation Buttons
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
