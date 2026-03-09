import streamlit as st
import pandas as pd

st.title("⭐ Select Celebrity")

df = pd.read_excel("celebrities.xlsx")

# 清理列名
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "")

names = df["Name"].tolist()

selected = st.selectbox("Choose Celebrity", names)

celeb = df[df["Name"] == selected].iloc[0]

st.header(celeb["Name"])

st.write("**Nationality:**", celeb["Nationality"])
st.write("**Profession:**", celeb["Profession"])

st.write(celeb["Description"])

st.subheader("Style")
st.write(celeb["StyleTags"])
