from supabase import create_client
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_audit(lat, lon, commentaire):
    user = st.session_state.get("user")

    if user:
        supabase.table("audits").insert({
            "user_id": user.id,
            "latitude": lat,
            "longitude": lon,
            "commentaire": commentaire
        }).execute()