import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Styling Board", layout="wide")

st.title("Styling Board")

df = pd.read_excel("items.xlsx")
df["ItemID"] = df["ItemID"].astype(str)

board = st.session_state.get("board", [])

if len(board) == 0:

    st.write("Your styling board is empty.")

else:

    cols = st.columns(4)

    for i, item_id in enumerate(board):

        row = df[df["ItemID"] == item_id].iloc[0]

        with cols[i % 4]:

            image_path = os.path.join("images", f"{item_id}.jpg")

            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)

            st.markdown(f"**{row['Brand']}**")
            st.write(row["Name"])
