import streamlit as st
from db import supabase

def signup_ui():
    st.title("Créer un compte")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Créer compte"):
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        st.success("Compte créé ✅")


def login_ui():
    st.title("Connexion")

    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if res.user:
            st.session_state["user"] = res.user
            st.success("Connecté ✅")
        else:
            st.error("Erreur ❌")


def logout():
    st.session_state.clear()
    