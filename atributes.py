import streamlit as st
import numpy as np
import pandas as pd
import requests

# get the player name from the user's input
player = st.text_input(label='input player name')

# prediction URL ================================================
URL1 = 'https://market-value-api-om3gdzslta-ew.a.run.app/predict'
params = {
    'player_name': player,
}

# futdb URL =====================================================
# URL2 = 'futdb.app/search/player'
# params={
#     'player_name' : player
# }

prediction_data = requests.get(URL1, params=params)
# prediction_data
data = prediction_data.json()
# data

@st.cache
def get_dataframe_data():

    return pd.DataFrame.from_dict(data['features'])


df = get_dataframe_data()
hdf = df.assign(hack='').set_index('hack')


st.write(f"{player}'s attributes")
st.table(hdf)
