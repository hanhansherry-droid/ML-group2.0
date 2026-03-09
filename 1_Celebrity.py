import streamlit as st
import pandas as pd
from utils.data_loader import load_celebrities

st.title("Select Celebrity")

celebs = load_celebrities()

selected = st.selectbox(
    "Choose Celebrity",
    celebs["Name"]
)

celeb = celebs[celebs["Name"] == selected].iloc[0]

st.subheader(celeb["Name"])

st.write("Nationality:", celeb["Nationality"])
st.write("Profession:", celeb["Profession"])

st.write("Description")
st.write(celeb["Description"])

st.write("Style Tags")
st.write(celeb["StyleTags"])

st.session_state["celebrity"] = celeb["Name"]