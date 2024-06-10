import datetime
import joblib
from sklearn import pipeline
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import requests
import os
from utils.airports import airport_city_dict, aeroports,compagnies_aeriennes, get_city_name,compagnies_aeriennes_dict,carriersfull,airport_options


def hhmm_to_decimal(hours_minutes):
    hours, minutes = divmod(hours_minutes, 100)
    return hours + minutes / 60

def afficher_logo_compagnie(carrier):
    logo_path = os.path.join( f'assets/img/{carrier}.png')
    if os.path.exists(logo_path):
        st.image(logo_path, width=100)
    else:
        st.write(f"Logo non disponible pour la compagnie {carrier}")

model = joblib.load('modele.joblib')



# Charger l'image du logo
logo = Image.open("assets/img/logo.PNG")  # Assurez-vous que le fichier image se trouve dans le même répertoire que ce script

# Afficher la bannière avec le logo et le titre


col1, col2 = st.columns([1,1 ])

def hhmm_to_decimal(hours_minutes):
    hours, minutes = divmod(hours_minutes, 100)
    return hours + minutes / 60

with col2:
    st.title("Prevoir l'imprevisible")

    # Création d'un formulaire
    with st.form("Sélectionner une date de vol"):
        # Ajout d'un sélecteur de date
        selected_date = st.date_input("Date du vol")
        crs_dep_time = st.time_input("Heure de Départ", value=datetime.datetime.now().time())  # Modification effectuée ici
        arr_time = st.time_input("Heure d'arrivée", value=datetime.datetime.now().time())  # Modification effectuée ici
        carrier=st.selectbox("Compagnie Aérienne", carriersfull)
        origin=st.selectbox("Aéroport de départ", aeroports)
        dest=st.selectbox("Aéroport d'arrivée", aeroports)
        distance=st.text_input("Distance de vol en km")
        selected_carrier_key = compagnies_aeriennes_dict[carrier]

        # Ajout d'un bouton de soumission
        submitted = st.form_submit_button("Valider")

    # Décomposition de la date en différentes variables après la soumission du formulaire
    if submitted:
        # Convertir la date sélectionnée en objet datetime
        date_obj = datetime.datetime.strptime(str(selected_date), "%Y-%m-%d")

        # Extraire le jour de la semaine, le jour du mois et le mois
        day_of_week = date_obj.weekday() + 1
        day_of_month = date_obj.day
        year=date_obj.year
        month = date_obj.month
        crs_dep_time_decimal = hhmm_to_decimal(crs_dep_time.hour * 100 + crs_dep_time.minute)
        arr_time_decimal = hhmm_to_decimal(arr_time.hour * 100 + arr_time.minute)





with col1:
    st.image(logo, width=200)

    if submitted:
        # Création d'un DataFrame avec les nouvelles données
        new_data = pd.DataFrame({
            'MONTH': [month],
            'DAY_OF_MONTH': [day_of_month],
            'DAY_OF_WEEK': [day_of_week],
            'CARRIER': [selected_carrier_key],
            'ORIGIN': [origin],
            'DEST': [dest],
            'DISTANCE': [distance],
            'CRS_DEP_TIME_DECIMAL': [crs_dep_time_decimal],
            'CRS_ARR_TIME_DECIMAL': [arr_time_decimal]
        })

        # Utilisation du modèle pour faire une prédiction
        prediction = model.predict(new_data)
        afficher_logo_compagnie(selected_carrier_key)
        depart = get_city_name(origin).upper()
        arrivee=get_city_name(dest).upper()
        st.header(f"{depart} - {origin}")
        st.write(f"Date:  {day_of_month}/{month}/{year}")
        st.write("Heure de départ :", crs_dep_time.isoformat('minutes'))
        st.header(f"{arrivee} - {dest}")
        st.write(f"Date {day_of_month}/{month}/{year}")
        st.write("Heure d'arrivée :", arr_time.isoformat('minutes'))

        # Afficher le résultat de la prédiction
        if prediction[0] == 0:
            st.success("Avion à l'heure probable à 74%")
        else:
            st.error("Retard probable à 43 %. Veuillez vérifier les mises à jour de votre vol.")
        # Afficher les résultats


        st.write("Compagnie Aérienne : ",carrier)

        st.write("Distance de vol en km:  ",distance)
