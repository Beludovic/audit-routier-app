import streamlit as st
import pandas as pd
import os
from datetime import datetime
from db import engine
from auth import login
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(layout="wide")

# Login
if "user" not in st.session_state:
    login()
    st.stop()

st.sidebar.success(f"Connecté: {st.session_state['user']}")

PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

# Charger DB
try:
    df = pd.read_sql("SELECT * FROM audits", engine)
except:
    df = pd.DataFrame(columns=[
        "date","lat","lon","type","gravite","commentaire","photo"
    ])

menu = st.sidebar.radio("Menu", ["Saisie", "Dashboard"])

# ==========================
# SAISIE
# ==========================
if menu == "Saisie":

    st.title("📍 Audit terrain")

    with st.form("form"):
        lat = st.number_input("Latitude", value=6.37)
        lon = st.number_input("Longitude", value=2.43)

        type_pb = st.selectbox("Type", [
            "Nid de poule","Signalisation","Obstacle","Accident","Autre"
        ])

        gravite = st.slider("Gravité", 1, 5)

        commentaire = st.text_area("Commentaire")

        photos = st.file_uploader("Photos", accept_multiple_files=True)

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            filenames = []

            for photo in photos:
                fname = f"{datetime.now().timestamp()}.jpg"
                path = os.path.join(PHOTO_DIR, fname)
                with open(path, "wb") as f:
                    f.write(photo.getbuffer())
                filenames.append(fname)

            new_row = pd.DataFrame([{
                "date": datetime.now(),
                "lat": lat,
                "lon": lon,
                "type": type_pb,
                "gravite": gravite,
                "commentaire": commentaire,
                "photo": ",".join(filenames)
            }])

            new_row.to_sql("audits", engine, if_exists="append", index=False)

            st.success("Donnée enregistrée")

# ==========================
# DASHBOARD
# ==========================
if menu == "Dashboard":

    st.title("📊 Dashboard stratégique")

    if df.empty:
        st.warning("Pas de données")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Observations", len(df))
        col2.metric("Gravité moyenne", round(df["gravite"].mean(),2))
        col3.metric("Points critiques", len(df[df["gravite"]>=4]))

        # Carte avec clustering
        from folium.plugins import MarkerCluster

        m = folium.Map(location=[6.37, 2.43], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in df.iterrows():
            folium.Marker(
                [row["lat"], row["lon"]],
                popup=f"{row['type']} (G{row['gravite']})"
            ).add_to(marker_cluster)

        st_folium(m, width=900, height=500)

        # Pareto
        pareto = df["type"].value_counts().reset_index()
        pareto.columns = ["type", "count"]

        fig = px.bar(pareto, x="type", y="count", title="Analyse Pareto")
        st.plotly_chart(fig)

        # Table
        st.dataframe(df)