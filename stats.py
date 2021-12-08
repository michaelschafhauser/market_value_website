import streamlit as st
import numpy as np
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
import json
#from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import plotly.express as px

#load_dotenv()
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
#headers["X-AUTH-TOKEN"] = os.getenv("AUTH-TOKEN")
headers["X-AUTH-TOKEN"]="6ee5d299-299c-480c-ba52-514607532d6a"
headers["Content-Type"] = "application/json"

# get the player name from the user's input
player = st.text_input(label='Insert Player Name')

# prediction URL ================================================
URL1 = 'https://market-value-api-om3gdzslta-ew.a.run.app/predict'
params_url1 = {
    'player_name': player,
}

# get the data from our prediction api
prediction_data = requests.get(URL1, params=params_url1)
data = prediction_data.json()
"""
# 🎉 Player estimated Value 🎉
"""

st.metric("Predicted value in millions of euros", data['prediction'])

# futdb name search URL =========================================
URL2 = "https://futdb.app/api/players/search"

params_url2 = {'name': player}
api_call = json.dumps(params_url2)
resp = requests.post(URL2, headers=headers, data=api_call).json()
searched_player = resp['items'][0]
#searched_player

list_of_stats = ['name', 'age', 'height', 'weight']
stats_dictionary = {}
for stat in list_of_stats:
    stats_dictionary[stat] = str(searched_player[stat])

# futdb image search URL =========================================
URL3 = f"https://futdb.app/api/players/{searched_player['id']}/image"
player_photo = requests.get(URL3)
player_photo.url  #this line will provide a link to the photo

player = resp['items'][0]
#player

#{player['name']}
st.metric("Player name",player['name'])
#player['age']
#player['height']
#player['weight']
league_ref=player["league"]
nation_ref=player["nation"]
club_ref=player["club"]
#data["prediction"]

player_geo_information={}

# Nations =====================================================
from dict_country_club import country_dict
for i in range(len(country_dict)):
    if nation_ref == country_dict[i]["id"]:
        player_geo_information["Nationality"] = (country_dict[i]["name"])

# Leagues =====================================================
URL4 = "https://futdb.app/api/leagues/"
params_url4 = {'id': league_ref}
league_resp = requests.get(URL4, headers=headers, params=params_url4).json()
league_name=league_resp['items']
for i in range(len(league_name)):
    if league_ref==league_name[i]["id"]:
        player_geo_information["League"] = (league_name[i]["name"])

# Clubs =====================================================
from dict_country_club import club_dict
for i in range(len(club_dict)):
    if league_ref == club_dict[i]["league"] and club_ref == club_dict[i]["id"]:
        player_geo_information["Club"] = (club_dict[i]["name"])


df_geographic_loc = pd.DataFrame.from_dict(player_geo_information,
                                           orient="index",
                                           columns=['Player Stats'])



# Club Images ================================================
#URL6 = "https://futdb.app/api/clubs/{club_ref}}/image"
#club_image_resp = requests.get(URL6, headers=headers).json()
#club_image_resp


@st.cache
def get_player_stats():
    return pd.DataFrame.from_dict(stats_dictionary,
                                  orient='index',
                                  columns=['Player Stats'])


stats_df = get_player_stats()
#st.table(stats_df)

frames = [stats_df, df_geographic_loc]
df_concat = pd.concat(frames, sort=False)
df_concat=df_concat.drop(labels=['name'], axis=0)
df_concat = df_concat.rename({
    "age": "Age",
    "height": "Height (cm)",
    "weight": "Weight (kg)"
})
df_concat

@st.cache
def get_dataframe_data():
    return pd.DataFrame.from_dict(data['features'])


# RADAR CHART =======================================================
def generate_radar_chart():
    r = []
    theta = []
    for key, value in data['features'].items():
        r.append(value[0])
        theta.append(key)

    df = pd.DataFrame(dict(r=r, theta=theta))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    return fig


'''
# Player Atributes
'''

df = get_dataframe_data()
hdf = df.assign(hack='').set_index('hack')
st.table(hdf)

radar = generate_radar_chart()
st.write(radar)
