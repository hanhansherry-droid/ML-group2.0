import streamlit as st
import pandas as pd

st.title("Select Celebrity")

celebs = pd.read_excel("celebrities.xlsx")

selected = st.selectbox(
    "Choose Celebrity",
    celebs["Name"]
)

celeb = celebs[celebs["Name"] == selected].iloc[0]

st.subheader(celeb["Name"])

st.write(celeb["Description"])

st.write("Style:")
st.write(celeb["StyleTags"])
