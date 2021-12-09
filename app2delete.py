import streamlit as st
import numpy as np
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
import json
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import plotly.express as px

load_dotenv()
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["X-AUTH-TOKEN"] = os.getenv("AUTH-TOKEN")
#headers["X-AUTH-TOKEN"] = "6ee5d299-299c-480c-ba52-514607532d6a"
headers["Content-Type"] = "application/json"

# sidebar
st.sidebar.markdown(f"""
    # Football MVP
    """)

FONT_SIZE_CSS = f"""
<style>
h1 {{
    font-size: 64px !important;
}}
</style>
"""

players = pd.read_csv("players.csv")
players = players.drop_duplicates()

#st.selectbox("Search for a player... ", players)
player = st.selectbox("Search for a player... ", players)

# get the player name from the user's input
# player = st.text_input(label='Insert Player Name')

# prediction URL ================================================
URL1 = 'https://market-value-api-om3gdzslta-ew.a.run.app/predict'
params_url1 = {
    'player_name': player,
}

# get the data from our prediction api
prediction_data = requests.get(URL1, params=params_url1)
data = prediction_data.json()

#Title
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

# Player Stats DF
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
st.metric("Player name", player['name'])
#player['age']
#player['height']
#player['weight']
league_ref = player["league"]
nation_ref = player["nation"]
club_ref = player["club"]
#data["prediction"]


player_geo_information = {}
# Nations =====================================================
from dict_country_club import country_dict
for i in range(len(country_dict)):
    if nation_ref == country_dict[i]["id"]:
        player_geo_information["Nationality"] = (country_dict[i]["name"])

# Leagues =====================================================
URL4 = "https://futdb.app/api/leagues/"
params_url4 = {'id': league_ref}
league_resp = requests.get(URL4, headers=headers, params=params_url4).json()
league_name = league_resp['items']
for i in range(len(league_name)):
    if league_ref == league_name[i]["id"]:
        player_geo_information["League"] = (league_name[i]["name"])

# Clubs =====================================================
from dict_country_club import club_dict
for i in range(len(club_dict)):
    if league_ref == club_dict[i]["league"] and club_ref == club_dict[i]["id"]:
        player_geo_information["Club"] = (club_dict[i]["name"])


# Nº of Clubs represented =====================================================
#player_geo_information["Nº Clubs"] = [(data["transfer_history"]["receiving_club"].nunique)][0]
player_geo_information["Nº Clubs"] = str(len(
    set(data["transfer_history"]["receiving_club"])))

#Player Stats DF 2
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

# Concated Player Stats DF
frames = [stats_df, df_geographic_loc]
df_concat = pd.concat(frames, sort=False)
df_concat = df_concat.drop(labels=['name'], axis=0)
df_concat = df_concat.rename({
    "age": "Age",
    "height": "Height (cm)",
    "weight": "Weight (kg)",
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


import matplotlib.pyplot as plt


transfer_fee_values=[]
for i in range(len(data["transfer_history"]["transfer_fee"])):
    transfer_fee_values.append(data["transfer_history"]["transfer_fee"][i])

transfer_fee_years=[]
for i in range(len(data["transfer_history"]["season"])):
    transfer_fee_years.append(data["transfer_history"]["season"][i])

transfer_age=[]
for i in range(len(data["transfer_history"]["age"])):
    transfer_age.append(data["transfer_history"]["age"][i])

receiving_club = []
for i in range(len(data["transfer_history"]["receiving_club"])):
    receiving_club.append(data["transfer_history"]["receiving_club"][i])


df_transfer_values = pd.DataFrame(transfer_fee_values)
df_transfer_values = df_transfer_values.rename(columns={0: 'Transfer_Values'})

df_transfer_years = pd.DataFrame(transfer_fee_years)
df_transfer_years = df_transfer_years.rename(columns={0: 'Transfer_Years'})
df_transfer_years["Transfer_Years"]=df_transfer_years["Transfer_Years"].apply(lambda x : int(x[:4]))

df_transfer_age = pd.DataFrame(transfer_age)
df_transfer_age = df_transfer_age.rename(columns={0: 'Age'})

df_receiving_club = pd.DataFrame(receiving_club)
df_receiving_club = df_receiving_club.rename(columns={0: 'Receiving Club'})


df_all = pd.concat([df_transfer_years, df_transfer_values,df_transfer_age, df_receiving_club], axis=1)
n_of_digits = sum(c.isdigit() for c in data["prediction"])-1
age_counter = 2021 - df_all.Transfer_Years.iloc[-1]
df_all.loc[len(df_all.index)] = [
    2022,
    int(data['prediction'][4:4 + n_of_digits]),
    df_all.Age.iloc[-1]+age_counter,
    "-"
]

df_all

#plt.bar(df_all.Transfer_Years, df_all.Transfer_Values)
#fig=plt.gcf()
#st.pyplot(fig)

import altair as alt
import streamlit as st

#value_season = alt.Chart(df_all).mark_area(color="blue").encode(x='Transfer_Years',
#y='Transfer_Values').properties(width=600)

#st.altair_chart(value_season)

fig = px.area(
    df_all,
    x='Transfer_Years',
    y="Transfer_Values",
    #color="continent",
    #line_group="country",
    #text=y,
    range_x=[df_all['Transfer_Years'].min()-1, df_all['Transfer_Years'].max()+1]
)


st.plotly_chart(fig)
