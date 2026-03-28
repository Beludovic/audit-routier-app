import streamlit as st

def require_login():
    if "user" not in st.session_state:
        st.warning("Veuillez vous connecter")
        return False
    return True