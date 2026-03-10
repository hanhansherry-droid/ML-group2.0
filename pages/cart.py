import streamlit as st

st.title("🛍 Saved Looks")

cart = st.session_state.get("cart", [])

if len(cart) == 0:
    st.info("No items saved yet.")
else:

    for i, item in enumerate(cart):

        col1, col2 = st.columns([1,2])

        with col1:
            st.image(item["ImageURL"], use_container_width=True)

        with col2:
            st.markdown(f"**{item['Brand']}**")
            st.write(item["Name"])

            st.write("Note:", item["note"])

            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
