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


"""
# Player estimated Value 🎉
"""

st.metric("Predicted Value in GBP", data['prediction'])



# futdb name search URL =========================================
URL2 = "https://futdb.app/api/players/search"

params_url2 = {'name' : player}
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
player_photo.url #this line will provide a link to the photo

# image is broken
# st.image(player_photo.url, width=400)

# scraping does not seem to work
# response = requests.get(URL3)
# soup = BeautifulSoup(response.content, 'html.parser')
# picture = soup.find('img')
# picture

@st.cache
def get_player_stats():
    return pd.DataFrame.from_dict(stats_dictionary, orient='index', columns=['Player Stats'])

stats_df = get_player_stats()
st.table(stats_df)


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
