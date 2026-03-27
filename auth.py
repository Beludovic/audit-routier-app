import streamlit as st

users = {
    "agent": {"password": "1234", "role": "agent"},
    "admin": {"password": "admin", "role": "admin"}
}

def login():
    st.sidebar.title("Connexion")
    username = st.sidebar.text_input("Utilisateur")
    password = st.sidebar.text_input("Mot de passe", type="password")

    if st.sidebar.button("Se connecter"):
        if username in users and users[username]["password"] == password:
            st.session_state["user"] = username
            st.session_state["role"] = users[username]["role"]
            st.success("Connecté")
        else:
            st.error("Erreur de connexion")