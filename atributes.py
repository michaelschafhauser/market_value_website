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
data

# futdb URL =====================================================
URL2 = "https://futdb.app/api/players/search"

params_url2={'name' : player}
data = json.dumps(params_url2)
resp = requests.post(URL2, headers=headers, data=data).json()
player = resp['items'][0]
player
# player['name']
# player['age']
# player['height']
# player['weight']
# data.get('prediction')



@st.cache
def get_dataframe_data():
    return pd.DataFrame.from_dict(data['features'])

df = get_dataframe_data()
hdf = df.assign(hack='').set_index('hack')

st.write(f"{player}'s attributes")
st.table(hdf)
