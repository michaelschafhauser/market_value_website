import streamlit as st

import numpy as np
import pandas as pd
import streamlit as st
import numpy as np
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
import json

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
# print the selected hobby
#st.write("Your hobby is: ", hobby)

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["X-AUTH-TOKEN"] = "6ee5d299-299c-480c-ba52-514607532d6a"
headers["Content-Type"] = "application/json"

# get the player name from the user's input
#player = st.text_input(label='input player name')

# prediction URL ================================================
URL1 = 'https://market-value-api-om3gdzslta-ew.a.run.app/predict'
params_url1 = {
    'player_name': player,
}

# get the data from our prediction api
prediction_data = requests.get(URL1, params=params_url1)
data = prediction_data.json()
# data

# futdb URL =====================================================
URL2 = "https://futdb.app/api/players/search"

params_url2 = {'name': player}
api_call = json.dumps(params_url2)
resp = requests.post(URL2, headers=headers, data=api_call).json()
searched_player = resp['items'][0]
# searched_player['name']
# searched_player['age']
# searched_player['height']
# searched_player['weight']
# data['prediction']
list_of_stats = ['name', 'age', 'height', 'weight']
stats_dictionary = {}
for stat in list_of_stats:
    stats_dictionary[stat] = searched_player[stat]
stats_dictionary['predicted_value'] = data['prediction']
stats_dictionary


@st.cache
def get_player_stats():
    return pd.DataFrame.from_dict(stats_dictionary, orient='index')


stats_df = get_player_stats()
h_stats_df = stats_df.assign(hack='').set_index('hack')

st.table(h_stats_df)


@st.cache
def get_dataframe_data():
    return pd.DataFrame.from_dict(data['features'])


df = get_dataframe_data()
hdf = df.assign(hack='').set_index('hack')

st.write(f"{player}'s attributes")
st.table(hdf)
