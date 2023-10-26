# Import 
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import altair as alt
import os
import time 
import requests
from bs4 import BeautifulSoup
import folium
from folium.plugins import HeatMap
plt.rcParams['figure.max_open_warning'] = 100  # Définir le nombre maximal de figures à 50 








# info sur moi 
st.sidebar.markdown("<h3 style='blue: red;'>Qui je suis ?  </h3>", unsafe_allow_html=True)
st.sidebar.markdown("[GitHub](https://github.com/jeremy-jer)")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/jeremy-sellam-44b5691b7/)")
st.sidebar.text("Prenom : Jérémy")
st.sidebar.text("Nom : Sellam")
st.sidebar.text("Promo : 2025")
st.sidebar.text("Classe : BIA2")

# Code du Dataframe

# Import de la DF 2022
data_usa = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/62c20524-d442-46f5-bfd8-982c59763ec8", delimiter=";")
data_cara = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/5fc299c0-4598-4c29-b74c-6a67b0cc27e7", delimiter=";")
data_lieu = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/a6ef711a-1f03-44cb-921a-0ce8ec975995", delimiter=";")


# suppression des lignes ou les colonnes  contenant des valeurs manquantes 
data_usa = data_usa.dropna()
data_cara = data_cara.dropna()


# créer un new Df qui n'a plus de ligne = Non renseigné
data_usa = data_usa[data_usa["trajet"] != -1 ]
data_usa = data_usa[data_usa["trajet"] != 0 ]
data_usa = data_usa[data_usa["locp"] != -1 ]
data_usa = data_usa[data_usa["actp"] != -1 ]
data_usa = data_usa[data_usa["etatp"] != -1 ]
data_cara = data_cara[data_cara["atm"] != -1]
data_lieu = data_lieu[data_lieu["surf"] != -1]

# check si les suppressions ont bien été effectuées 
data_usa0 = data_usa[data_usa["trajet"] == 0 ]

# Pour le sexe, nous avons le 1 = Homme et 2 = Femme donc on remplace 
data_usa["sexe"] = data_usa["sexe"].replace({1 : "H", 2: "F"})

# Calculer l'âge 
annee_actuelle = pd.Timestamp.now().year
data_usa['age'] = annee_actuelle - data_usa['an_nais']

# Supprimer la colonne 'an_nais' car elle ne sert plus à rien
data_usa = data_usa.drop(columns=['an_nais'])



# nombre de personne qui a moins -25ans et qui conduit  = 9  = 0.13%
data_usa_Jeune = len(data_usa[(data_usa["place"] == 1) & (data_usa["age"] < 25)])
pourcentage_mort_jeune = round((data_usa_Jeune/len(data_usa)) * 100,2)

# nb de personnes qui conduises et qui ont plus de 25 ans = 0.87%
data_usa_Vieux = 1 - pourcentage_mort_jeune


#  Voir le nombre d'Homme dans mon Df = 3291
nb_H = len(data_usa[data_usa["sexe"] == "H"])

 # Afficher le pourcentage = 48.76
Pourcentage_Acc_H = round((nb_H/len(data_usa)) *100, 2)

# Pareil pour les femmes = 51.24
nb_F = len(data_usa[data_usa["sexe"] == "F"])
Pourcentage_Acc_F = round((nb_F/len(data_usa)) *100, 2)

# Verif que j'obtiens bien 100% : j'ai bien 100%
# print("La somme des nb vaut:", Pourcentage_Acc_H + Pourcentage_Acc_F, "%") 

# On va s'occuper de la place "du mort"
# voir quelles sont les valeurs possibles 
valeurs_uniques_place = data_usa['place'].unique()

# Pourcentage place coté passager  = 3 = 0.04%
mort_place = len(data_usa[data_usa["place"] == 2])
pourcentage_mort_place = round((mort_place / len(data_usa)) *100, 2)

# Pourcentage place arrière derniere le coté passager = 1 = 0.01%
place_arriere_cote_passage = len(data_usa[data_usa["place"] == 3])
pourcentage_place_arriere_cote_passage = round((place_arriere_cote_passage / len(data_usa)) * 100, 2)

# place conducteur = 29 = 0.43 %
place_conducteur = len(data_usa[data_usa["place"] == 1])
pourcentage_place_conducteur = round((place_conducteur/len(data_usa)) *100, 2)

# mort pieton  = 6717 =  99.51%
pieton = len(data_usa[data_usa["place"] == 10])
pourcentage_pieton = round((pieton/len(data_usa)) *100, 2)


# Personnes sans sécu = 46.23% (2777 lignes)
data_sans_secur = data_usa[(data_usa["secu1"].isin([0, -1])) & (data_usa["secu2"].isin([0, -1])) & (data_usa["secu3"].isin([0, -1]))]
nombre_personnes_moins_de_40_ans = data_sans_secur[data_sans_secur["age"] < 40].shape[0]

# Calcul du pourcentage
pourcentage_mort_des_personnes_sans_secu_de_moins_de_40_ans = round((nombre_personnes_moins_de_40_ans/len(data_sans_secur)) *100, 2)

# plus de 40 ans 
nombre_personnes_plus_de_40_ans = data_sans_secur[data_sans_secur["age"] > 40].shape[0]
pourcentage_mort_des_personnes_sans_secu_de_plus_de_40_ans = round((nombre_personnes_plus_de_40_ans/len(data_sans_secur)) *100, 2)

# Nouveau DataFrame avec au moins une sécurité = 53.77%
data_avec_secur = data_usa[(data_usa["secu1"].isin([0, -1])) | (data_usa["secu2"].isin([0, -1])) | (data_usa["secu3"].isin([0, -1]))]
nombre_personnes_moins_de_40_ans_avec_secur = data_avec_secur[data_avec_secur["age"] < 40].shape[0]


# Calcul du pourcentage
pourcentage_mort_des_personnes_avec_secu_de_moins_de_40_ans = round((nombre_personnes_moins_de_40_ans_avec_secur/len(data_avec_secur)) *100, 2)

#Plus de  40 ans 
nombre_personnes_plus_de_40_ans_avec_secur = data_avec_secur[data_avec_secur["age"] > 40].shape[0]
pourcentage_mort_des_personnes_avec_secu_de_plus_de_40_ans = round((nombre_personnes_plus_de_40_ans_avec_secur/len(data_avec_secur)) *100, 2)







# --------------------------------------------------------------------------------------------------------------
# Inserer l'image 

image = Image.open('image.jpg')
st.image(image, caption="Acccident de voiture")

# titre de la page web
st.markdown("<h1 style='color: black;'>Les accidents de voiture </h1>", unsafe_allow_html=True)


# Premiere question que je veux vérifier
# Le unsafe_allow_html=True permet d'accepter le HTML depuis streamlit
st.markdown("""
    <div style='text-align:center'>
        <h2>Préjugés, Stéréotypes, vrais ?</h2>
    </div>
""", unsafe_allow_html=True)

print("\n")


# -------------------------------------------------------------------------------------------------------------------------------------------------
# Widget 

# Menu déroulant 
choix_1 = st.selectbox("Croyez-vous que les stéréotypes et les préjugés soient vrais ?", ["Oui", "Non", "Je ne sais pas"])

# Afficher le choix sélectionné
st.write("Vous avez choisi:", choix_1)

## Bouton Valider
if st.button("Valider", key="valider_1"):
    # Afficher une animation de succès
    with st.spinner("Traitement en cours..."):
        time.sleep(2) 

    # Afficher un message de succès
    st.success("Merci pour votre réponse !")

# --------------------------------------------------------------------------------------------------------------

st.subheader("1) Quel est le sexe à faire le plus d'accident ? ")

# Création d'un petit questionnaire pour vérifier les connaissances
# Le premier argument = titre du questionnaire, et le second = option du bouton
Question_sexe_accident = st.radio("Selon vous ce sont les : ", ('Hommes', 'Femmes'))

st.subheader("Graphique qui montre")


# Afficher un graphique à barre pour représenter mieux les pourcentages 
colonnes = ['H', 'F']
pourcentages = [Pourcentage_Acc_H, Pourcentage_Acc_F]
st.bar_chart(pourcentages)
st.write("Répartition des accidents en fonction des sexes en %")
st.write(f"- Hommes : {pourcentages[0]}%")
st.write(f"- Femmes : {pourcentages[1]}%")

# 2ème partie des stéréotypes : 
# La place du mort (juste à coté du condacteur)

# Données pour le camembert
labels = ['1 ', '2', '3', '4']
PourcentagesCam = [pourcentage_mort_place, pourcentage_place_arriere_cote_passage,pourcentage_place_conducteur , pourcentage_pieton]

# --------------------------------------------------------------------------------------------------------------


st.subheader("2) Les morts par leur position dans un transport ?")

st.write("Passez votre souris au dessus pour voir les %")

# Données pour le camembert
data = pd.DataFrame({
    'labels': ['1', '2', '3', '4'],
    'PourcentagesCam': [pourcentage_mort_place, pourcentage_place_arriere_cote_passage, pourcentage_place_conducteur, pourcentage_pieton]
})

# Créer le camembert
chart = alt.Chart(data).mark_arc().encode(
    color='labels:N',
    theta='PourcentagesCam',
    tooltip=['labels', 'PourcentagesCam']
).properties(
    width=400,
    height=400
)

# Afficher le camembert
st.altair_chart(chart)

# Ajoutez une légende pour expliquer le camembert
st.text("Explication du camembert :")
st.text("- 'place coté passager' représente 0.04% = bleue foncé ")
st.text("- 'place arrière dernière le coté passager' représente 0.01% = bleu clair ")
st.text("- 'place conducteur' représente 0.43% = rouge ")
st.text("- 'piéton' représente 99.51% = rose/bège")

# Partie de zoom du camembert
st.subheader("Nous allons maintenant faire un zoom sur la partie qui n'est pas trop visible.")
st.subheader("Ainsi, voir le % de la partie qu'on ne voit pas trop.")
data_zoom = pd.DataFrame({
    'labels_zoom': ['1', '2', '3'],
    'PourcentagesCam_zoom': [pourcentage_mort_place, pourcentage_place_arriere_cote_passage, pourcentage_place_conducteur]
})

# Créer le camembert
chart_zoom = alt.Chart(data_zoom).mark_arc().encode(
    color='labels_zoom:N',
    theta='PourcentagesCam_zoom',
    tooltip=['labels_zoom', 'PourcentagesCam_zoom']
).properties(
    width=400,
    height=400
)

# Afficher le camembert
st.altair_chart(chart_zoom)



# Créez le graphique 
st.subheader("Etat des personnes en fonction de leur âge ")
st.write("Légende:")
st.write("- 1 : indemne")
st.write("- 2 : tué")
st.write("- 3 : blessé hospitalisé")
st.write("- 4 : blessé léger")
st.write("Ordonnée = nombre de cas qui associe grave et l'age ")
st.write("Abscisse = Age")
st.line_chart(data_usa.groupby(['age', 'grav']).size().unstack(), use_container_width=True)

# --------------------------------------------------------------------------------------------------------------


st.subheader("3) Qui fait le plus d'accident entre les jeunes et les vieux ")

Question_age_accident = st.radio("Selon vous ce sont les : ", ("-40 ans", ' +40 ans '))

st.info("Dans mon analyse, il y a plus de + 40 ans")

st.write("Représente une absence d'une sécurité")

# Données pour le camembert
data_sans_secu = pd.DataFrame({
    'labels_sans_secu': ['moins de 40 ans', "plus de 40 ans"],
    'Pourcentages_mort': [pourcentage_mort_des_personnes_sans_secu_de_moins_de_40_ans, pourcentage_mort_des_personnes_sans_secu_de_plus_de_40_ans]
})

# Créer le camembert
chart_sans_secu = alt.Chart(data_sans_secu).mark_arc().encode(
    color='labels_sans_secu',
    theta='Pourcentages_mort',
    tooltip=['labels_sans_secu', 'Pourcentages_mort']
).properties(
    width=400,
    height=400
)

st.altair_chart(chart_sans_secu)

st.write("Représente la présence d'une sécurité quelconque")

# Données pour le camembert
data_avec_secu = pd.DataFrame({
    'labels_avec_secu': ['moins de 40 ans', "plus de 40 ans"],
    'Pourcentages_mort': [pourcentage_mort_des_personnes_avec_secu_de_moins_de_40_ans, pourcentage_mort_des_personnes_avec_secu_de_plus_de_40_ans]
})



# Créer le camembert
chart_avec_secu = alt.Chart(data_avec_secu).mark_arc().encode(
    color='labels_avec_secu',
    theta='Pourcentages_mort',
    tooltip=['labels_avec_secu', 'Pourcentages_mort']
).properties(
    width=400,
    height=400
)

st.altair_chart(chart_avec_secu)

# --------------------------------------------------------------------------------------------------------------


st.subheader("4) Le rapport entre le trajet et les accidents ")

# Titre de l'application
st.text("Nombre de Trajets en fonction de la Gravité")

# Grouper les données par trajet et gravité, puis compter le nombre d'occurrences
# unstack = déroule les niveaux d'index pour créer une structure tabulaire = afficher les diff grav
groupe_trajet_grave = data_usa.groupby(['trajet', 'grav']).size().unstack(fill_value=0) 

# Créer le graphique en barres
fig, ax = plt.subplots()
groupe_trajet_grave.plot(kind='bar', ax=ax)
plt.xlabel('Type de Trajet')
plt.ylabel('Nombre de Trajets')
plt.legend(title='Gravité en fonction des trajets', labels=['Indemne', 'Tué', 'Blessé hospitalisé', 'Blessé léger'])

message = """
- 1 – Domicile – travail
- 2 – Domicile - école
- 3 Courses – achats
- 4 – Utilisation professionnelle
- 5 – Promenade – loisirs
- 9 – Autre
"""

st.warning(message)

# Afficher le graphique dans Streamlit
st.pyplot(fig)

# --------------------------------------------------------------------------------------------------------------

st.subheader("5) Les actions des piétons ")

# Mettre dans notre DF seulement les valeurs utiles 
action_pieton = data_usa[(data_usa['catu'] == 3) & (data_usa['actp'] != 0) & (data_usa['actp'] != -1) & (data_usa["actp"] != "B")]

# Combiner les colonnes action et graves
action_counts = action_pieton.groupby(['actp', 'grav']).size().unstack().fillna(0)

# Affichage 
st.subheader("actions des piétons par gravité")

# Création d'une nvll figure et empiler les barres 
fig, ax = plt.subplots()
action_counts.plot(kind='bar', stacked=True, ax=ax)

# Ajout de la légende
plt.legend(["Indemne", "Tué", "Blessé hospitalisé", "Blessé léger"])

message = """
- 1 – Sens véhicule heurtant 
- 2 – Sens inverse du véhicule
- 3 – Traversant 
- 4 – Masqué 
- 5 – Jouant – courant 
- 6 – Avec animal 
- 9 – Autre 
- A – Monte/descend du véhicule 
"""

st.warning(message)

# Affichage du graphique avec Streamlit
st.pyplot(fig)


# -------------------------------------------------------------------------------------------------------------


# Filtrer les données pour ne garder que les piétons
pietons = data_usa[data_usa['catu'] == 3]

# Compter les occurrences de chaque état
Nombre = pietons['etatp'].value_counts()

# Afficher les résultats
st.write("Répartition de l'état des piétons :")
st.write(Nombre)

# Créer un graphique pour visualiser l'état des piétons
st.bar_chart(Nombre)

# Afficher la légende
st.write("Légende de l'état des piétons:")
st.write("1: Seul")
st.write("2: Accompagné")
st.write("3: En groupe")




# ------------------------------------------------------------------------------------------------------------


st.subheader("6) Types de véhicules impliqués par gravité")

data_types_vehicules = data_usa[['num_veh', 'grav']]

# Compter les occurrences de chaque type de véhicule par gravité
type_vehicule_counts = data_types_vehicules.groupby(['num_veh', 'grav']).size().unstack(fill_value=0)

# Création d'une nouvelle figure et empiler les barres
fig, ax = plt.subplots()
type_vehicule_counts.plot(kind='bar', stacked=True, ax=ax)

# Ajout de la légende
plt.legend(["Indemne", "Tué", "Blessé hospitalisé", "Blessé léger"])

# Ajouter un titre et des étiquettes aux axes
plt.xlabel('Type de Véhicule')
plt.ylabel('Nombre d\'Accidents')

# Afficher le graphique dans Streamlit
st.pyplot(fig)
# --------------------------------------------------------------------------------------------------------------


# Extrait les heures et les minutes de la colonne 'hrmn'
data_cara['heure'] = data_cara['hrmn'].str.split(':').str[0].astype(int)
data_cara['minute'] = data_cara['hrmn'].str.split(':').str[1].astype(int)

# Calcule le total des minutes
data_cara['total_minutes'] = data_cara['heure'] * 60 + data_cara['minute']

# Détermine si l'accident a lieu pendant les heures de pointe
heures_pointe = (data_cara['total_minutes'] >= 420) & (data_cara['total_minutes'] <= 540) | (data_cara['total_minutes'] >= 1020) & (data_cara['total_minutes'] <= 1140)

# Compte le nombre d'accidents 
accidents_heures_pointe = len(data_cara[heures_pointe])
accidents_hors_pointe = len(data_cara[~heures_pointe])

# Calcule le pourcentage 
pourcentage_heures_pointe = round((accidents_heures_pointe / (accidents_heures_pointe + accidents_hors_pointe)) * 100, 2)

st.subheader("7) Les heures de pointe impactent-elles les accidents ")

# Affiche les résultats
st.markdown("### Résultats :")
st.write(f"Nombre d'accidents pendant les heures de pointe : {accidents_heures_pointe}")
st.write(f"Nombre d'accidents en dehors des heures de pointe : {accidents_hors_pointe}")
st.write(f"Pourcentage d'accidents pendant les heures de pointe : {pourcentage_heures_pointe}%")


# -----------------------------------------------------------------------------------------------------------------------
# Correspondance entre les codes et les états de surface


st.subheader("8) La méteo et son impact")
message = """
- 1 Normale',
- 2: 'Mouillée',
- 3: 'Flaques',
- 4: 'Inondée',
- 5: 'Enneigée',
- 6: 'Boue',
- 7: 'Verglacée',
- 8: 'Corps gras – huile',
- 9: 'Autre' 
"""

st.info(message)

st.subheader("Pour toi quel type de météo impacte le plus les accidents sachant que mon analyse porte sur 2022")

# Définir les options pour le menu déroulant
options = {
    1: 'Normale',
    2: 'Mouillée',
    3: 'Flaques',
    4: 'Inondée',
    5: 'Enneigée',
    6: 'Boue',
    7: 'Verglacée',
    8: 'Corps gras – huile',
    9: 'Autre'
}

# Afficher le menu déroulant
choix = st.selectbox("Sélectionnez l'état de la surface :", options)

if st.button("Valider"):
    # Filtrer les données en fonction de l'option sélectionnée
    surface_filtree = data_lieu[data_lieu['surf'] == choix]

    # Calcul du nombre d'accidents 
    accidents_par_surface = surface_filtree['surf'].value_counts()

    # Création d'un graphique à barres
    plt.figure(figsize=(10, 6))
    accidents_par_surface.plot(kind='bar')
    plt.title(f'Nombre d\'accidents selon l\'état de la surface : {options[choix]}')
    plt.xlabel('État de la surface')
    plt.ylabel('Nombre d\'accidents')

    st.pyplot(plt)

# Réponse : 

st.subheader("Réponse ")

type_surface = {
    -1: 'Non renseigné',
    1: 'Normale',
    2: 'Mouillée',
    3: 'Flaques',
    4: 'Inondée',
    5: 'Enneigée',
    6: 'Boue',
    7: 'Verglacée',
    8: 'Corps gras – huile',
    9: 'Autre'
}

# Remplace les codes par les états de surface
data_lieu['surf'] = data_lieu['surf'].replace(type_surface)

# Calcul du nombre d'accidents 
accidents_par_surface = data_lieu['surf'].value_counts()

# Création d'un graphique à barres
plt.figure(figsize=(10, 6))
accidents_par_surface.plot(kind='bar')
plt.title('Nombre d\'accidents selon l\'état de la surface')
plt.xlabel('État de la surface')
plt.ylabel('Nombre d\'accidents')

# Affichage du graphique
st.pyplot(plt)

#----------------------------------------------------------------------------------------------------------------

# Créer un menu déroulant
choix = st.selectbox("Concernant les stéréotypes, avez-vous changé d'avis ?", ["Oui", "Non", "Je ne sais pas"])

# Afficher le choix sélectionné
st.write("Vous avez choisi:", choix)

## Bouton Valider
if st.button("Valider", key="valider_2"):
    # Afficher une animation de succès
    with st.spinner("Traitement en cours..."):
        time.sleep(2) 

    # Afficher un message de succès
    st.success("Merci pour votre réponse !")









