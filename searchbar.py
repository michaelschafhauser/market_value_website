import streamlit as st

import numpy as np
import pandas as pd


players = pd.read_csv("players.csv")
players = players.drop_duplicates()

st.selectbox("Search for a player... ", players)
# print the selected hobby
#st.write("Your hobby is: ", hobby)
