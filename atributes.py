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
# data

# futdb name search URL =====================================================
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
stats_dictionary['predicted_value_millions'] = data['prediction']

# futdb image search URL ===================================================
URL3 = f"https://futdb.app/api/players/{searched_player['id']}/image"
player_photo = requests.get(URL3, headers=headers)
player_photo.url #this line will provide a link to the photo


a = f"""Some text

![Cool Image]({player_photo.url})

Some more text"""

st.markdown(a)


st.image(str(player_photo.url), width=400)
st.image('https://cdn-images-1.medium.com/max/1024/1*u9U3YjxT9c9A1FIaDMonHw.png')


@st.cache
def get_player_stats():
    return pd.DataFrame.from_dict(stats_dictionary, orient='index', columns=['Player Stats'])

stats_df = get_player_stats()
st.table(stats_df)
# micheal deleted my file schiesse


@st.cache
def get_dataframe_data():
    return pd.DataFrame.from_dict(data['features'])

df = get_dataframe_data()
hdf = df.assign(hack='').set_index('hack')

st.write(f"{player}'s attributes")
st.table(hdf)
