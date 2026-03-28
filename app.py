import streamlit as st
from auth import login_ui, signup_ui, logout
from db import insert_audit
from utils import require_login

st.set_page_config(page_title="Audit Routier", layout="wide")

menu = st.sidebar.selectbox("Menu", ["Connexion", "Créer un compte"])

if menu == "Connexion":
    login_ui()

elif menu == "Créer un compte":
    signup_ui()

# ---------------- APP ----------------
if require_login():

    st.title("🚧 Audit Routier")

    if st.sidebar.button("Se déconnecter"):
        logout()

    lat = st.number_input("Latitude")
    lon = st.number_input("Longitude")
    commentaire = st.text_area("Commentaire")

    if st.button("Enregistrer"):
        insert_audit(lat, lon, commentaire)
        st.success("Audit enregistré ✅") 