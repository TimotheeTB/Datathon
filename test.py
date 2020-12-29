import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import folium

st.write("""
# Mon petit coin de paradis
""")

databrochet =pd.read_csv("file:///Users/timothee/Desktop/Wild%20Code%20School/drive-download-20201120T125440Z-001/datamaquereau.csv",index_col='Code_commune')
databrochet.drop(columns="COM",inplace=True)

databreme = pd.read_csv('file:///Users/timothee/Desktop/Wild%20Code%20School/drive-download-20201120T125440Z-001/databrème%20(1).csv')
databreme.set_index('Code_commune', inplace = True)

# On definit nos metrics

def cosine_sim(a,b):
    dot_product=np.dot(a,b)
    norma=np.linalg.norm(a)
    normb=np.linalg.norm(b)
    return dot_product/(norma*normb)

def cosine_distance(a,b):
    return 1-cosine_sim(a,b)

def euclid(a,b):
    return np.sqrt(np.sum((a-b)**2))

# Calcule les "nb_sortie" plus petites distances d'apres la metrique "metric" entre le vecteur "user" et toutes
# les lignes du dataframe "cities"

def least_distance(cities,user,nb_sortie,metric):
    arr=np.zeros(len(cities.index))
    for i in range(len(cities.index)):
        arr[i]=metric(user,cities.iloc[i])
    return pd.Series(arr).sort_values().head(nb_sortie)

# Renvoie les lignes du dataframe cities qui correspondent aux lignes sorties par least_distance

def best_matches(cities,user, nb_sortie,metric):
    return cities.iloc[least_distance(cities,user,nb_sortie,metric).index]

st.sidebar.header("Critères de l'utilisateur")

def userinput():

    user=np.zeros(8)

    Code_Pop=st.sidebar.select_slider("Nombre d'habitants de la ville", options = ['Entre 0 et 500', 'Entre 501 et 1 000', 'Entre 1 001 et 5 000', 'Entre 5 001 et 10 000', 'Entre 10 001 et 50 000', 'Entre 50 001 et 100 000', 'Supérieur à 100 000'])
    mapping={'Entre 0 et 500':1,'Entre 501 et 1 000':2,'Entre 1 001 et 5 000':3,'Entre 5 001 et 10000':4,'Entre 10 001 et 50 000':5,'Entre 50 001 et 100 000':6,'Supérieur à 100 000':7}
    codepop=int(mapping[Code_Pop])

    Code_Santé=st.sidebar.slider("Importance de la santé (1 à 5)",1, 5)
    user[0]=int(Code_Santé)


    Code_Resto=st.sidebar.slider("Présence de la restauration (1 à 5)",1, 5)
    user[1]=int(Code_Resto)

    Code_ServicesP=st.sidebar.slider("Services publiques (1 à 5)",1, 5)
    user[2]=int(Code_ServicesP)

    Code_Services=st.sidebar.slider("Autres services (1 à 5)",1, 5)
    user[3]=int(Code_Services)


    Code_Transport=st.sidebar.slider("Présence des transports (1 à 5)",1, 5)
    user[4]=int(Code_Transport)

    Code_Activité=st.sidebar.slider("Loisirs (1 à 5)",1, 5)
    user[5]=int(Code_Activité)


    Code_Connexion=st.sidebar.slider("Couverture haut-débit (1 à 5)",1, 5)
    user[6]=int(Code_Connexion)


    Code_Prix=st.sidebar.slider("Prix au m2 (1 à 5)",1, 5)
    user[7]=Code_Prix

    print(codepop)
    print(user)
    print(type(codepop))
    print(type(user))

    return (codepop,user)



def user_result(cities,nb_sortie,metric):
    codepop,user=userinput()
    print("a")
    temp=cities[cities["NotePop"]==codepop].drop(columns="NotePop")
    print("b")
    return best_matches(temp,user,nb_sortie,metric)

databrochet=databrochet.loc[databrochet.index.isin(databreme.index)]

def geo(ind):
    return databreme.loc[databreme.index.isin(ind)]

a=user_result(databrochet,5,euclid)

st.write(a)

df_geo = geo(a.index).copy()
df_geo.drop(columns="Unnamed: 0",inplace=True)
df_geo.rename(columns={"long":"lon"},inplace=True)

st.write(df_geo)

locations = df_geo[['lat', 'lon']]
locationlist = locations.values.tolist()
loc2=locations.reset_index(drop=True)

carte = folium.Map(location=locationlist[4], zoom_start = 6)
for point in range(0, len(locationlist)):
    folium.Marker(locationlist[point], popup=df_geo['COM'][point]).add_to(carte)

folium_static(carte)
