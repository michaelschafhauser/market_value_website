import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from data import get_player_data, get_futdb_data
import requests
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
import os

# HEADERS ==================================

load_dotenv()
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["X-AUTH-TOKEN"] = os.getenv("AUTH-TOKEN")
headers["Content-Type"] = "application/json"

# URLS ======================================
URL4 = "https://futdb.app/api/leagues/"

# sidebar =================================
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

player = st.selectbox("Search for a player... ", players)


# prediction URL =================================
data = get_player_data(player)

"""
# 🎉 Player estimated Value 🎉
"""
st.metric("Predicted value", data['prediction'])

# futdb name search URL =========================================
searched_player = get_futdb_data(player)
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


st.metric("Player name", searched_player['name'])
league_ref = searched_player["league"]
nation_ref = searched_player["nation"]
club_ref = searched_player["club"]



# NATIONS, LEAGUES, CLUBS ====================================
player_geo_information = {}

from dict_country_club import country_dict
for i in range(len(country_dict)):
    if nation_ref == country_dict[i]["id"]:
        player_geo_information["Nationality"] = (country_dict[i]["name"])

params_url4 = {'id': league_ref}
league_resp = requests.get(URL4, params=params_url4, headers=headers).json()
league_name = league_resp['items']
for i in range(len(league_name)):
    if league_ref == league_name[i]["id"]:
        player_geo_information["League"] = (league_name[i]["name"])

from dict_country_club import club_dict
for i in range(len(club_dict)):
    if league_ref == club_dict[i]["league"] and club_ref == club_dict[i]["id"]:
        player_geo_information["Club"] = (club_dict[i]["name"])

# Player Stats DF 2
df_geographic_loc = pd.DataFrame.from_dict(player_geo_information,
                                           orient="index",
                                           columns=['Player Stats'])

# ================================================================


@st.cache
def get_player_stats():
    return pd.DataFrame.from_dict(stats_dictionary, orient='index', columns=['Player Stats'])


stats_df = get_player_stats()

# Concated Player Stats DF
frames = [stats_df, df_geographic_loc]
df_concat = pd.concat(frames, sort=False)
df_concat = df_concat.drop(labels=['name'], axis=0)
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
    r=[]
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
