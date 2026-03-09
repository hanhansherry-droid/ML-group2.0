import streamlit as st

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    page_icon="✨",
    layout="wide"
)

st.title("AI Celebrity Styling Platform")

st.write("Welcome to the styling platform.")

st.write("")

st.subheader("Start Styling")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_Celebrity.py", label="Select Celebrity", icon="⭐")

with col2:
    st.page_link("pages/Select_Clothing.py", label="Browse Clothing", icon="👗")

st.write("")

st.subheader("Workflow")

st.write("""
1. Select Celebrity  
2. Filter Clothing  
3. Generate Sample Request Email
""")
