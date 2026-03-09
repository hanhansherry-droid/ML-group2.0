import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Celebrity Styling Platform",
    layout="wide"
)

# ======================
# CSS 美化
# ======================

st.markdown("""
<style>

body {
    background-color: white;
}

.header{
    font-size:40px;
    font-weight:600;
    text-align:center;
}

.subtitle{
    font-size:20px;
    text-align:center;
    color:gray;
}

.center-button{
    text-align:center;
}

.product-card{
    border-radius:10px;
    padding:10px;
    background:#f7f7f7;
}

</style>
""", unsafe_allow_html=True)

# ======================
# 顶部导航
# ======================

nav1,nav2,nav3 = st.columns([1,4,1])

with nav1:
    st.write("☰ Menu")

with nav2:
    st.markdown("<h1 style='text-align:center'>AI STYLING</h1>", unsafe_allow_html=True)

with nav3:
    st.write("❤ Cart")

st.divider()

# ======================
# Banner
# ======================

st.image(
    "https://images.unsplash.com/photo-1490481651871-ab68de25d43d",
    use_container_width=True
)

st.markdown("<div class='header'>AI Celebrity Styling Platform</div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Discover fashion pieces for celebrity styling</div>", unsafe_allow_html=True)

st.write("")

btn1,btn2 = st.columns(2)

with btn1:
    if st.button("Start Styling"):
        st.switch_page("pages/1_Celebrity.py")

with btn2:
    if st.button("Browse Collection"):
        st.switch_page("pages/Select_Clothing.py")

st.write("")
st.write("")

# ======================
# 商品展示
# ======================

st.header("New Collection")

df = pd.read_excel("items.xlsx")

cols = st.columns(4)

for i,row in df.head(8).iterrows():

    with cols[i % 4]:

        st.image(row["ImagePath"])

        st.write(row["Name"])

        st.caption(row["Brand"])

