import streamlit as st
import numpy as np
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
import json

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["X-AUTH-TOKEN"] = "6ee5d299-299c-480c-ba52-514607532d6a"
headers["Content-Type"] = "application/json"


# get the player name from the user's input
player = st.text_input(label='input player name')

# prediction URL ================================================
URL1 = 'https://market-value-api-om3gdzslta-ew.a.run.app/predict'
params_url1 = {
    'player_name': player,
}

# get the data from our prediction api
prediction_data = requests.get(URL1, params=params_url1)
data = prediction_data.json()
#data

# futdb URL =====================================================
URL2 = "https://futdb.app/api/players/search"

params_url2 = {'name': player}
data2 = json.dumps(params_url2)
resp = requests.post(URL2, headers=headers, data=data2).json()

player = resp['items'][0]
#player
player['name']
player['age']
player['height']
player['weight']
league_ref=player["league"]
nation_ref=player["nation"]
club_ref=player["club"]
data["prediction"]

player_geo_information={}

# Nations =====================================================
from dict_country_club import country_dict
for i in range(len(country_dict)):
    if nation_ref == country_dict[i]["id"]:
        player_geo_information["Nationality"]=(country_dict[i]["name"])

# Leagues =====================================================
URL3 = "https://futdb.app/api/leagues/"
params_url3 = {'id': league_ref}
league_resp = requests.get(URL3, headers=headers, params=params_url3).json()
league_name=league_resp['items']
for i in range(len(league_name)):
    if league_ref==league_name[i]["id"]:
        player_geo_information["League"] = (league_name[i]["name"])

# Clubs =====================================================
from dict_country_club import club_dict
for i in range(len(club_dict)):
    if league_ref == club_dict[i]["league"] and club_ref == club_dict[i]["id"]:
        player_geo_information["Club"] = (club_dict[i]["name"])

df=pd.DataFrame.from_dict(player_geo_information,orient="index")
df

# Club Images ================================================
#URL6 = "https://futdb.app/api/clubs/{club_ref}}/image"
#club_image_resp = requests.get(URL6, headers=headers).json()
#club_image_resp


@st.cache
def get_dataframe_data():
    return pd.DataFrame.from_dict(data['features'])


df = get_dataframe_data()
hdf = df.assign(hack='').set_index('hack')

st.write("Player's attributes")
st.table(hdf)
