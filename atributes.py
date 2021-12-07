import streamlit as st
import numpy as np
import pandas as pd

#ronaldo attributes
ronaldo = [91, 91, 88, 94, 83, 90, 35, 78]

# get the player attributes from the predict.py
fetched_player = [91, 91, 88, 94, 83, 90, 35, 78]


@st.cache
def get_dataframe_data():
    columns = ['overall', 'potential', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical']

    return pd.DataFrame([fetched_player], columns=columns)


df = get_dataframe_data()
hdf = df.assign(hack='').set_index('hack')


st.write('player attributes')
st.table(hdf)

# pip install market value predictor
# use it as a requirement
# look at get_player_features
#
