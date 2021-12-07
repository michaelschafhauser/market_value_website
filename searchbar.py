import streamlit as st

import numpy as np
import pandas as pd

st.sidebar.markdown(f"""
    # Football MVP
    """)

FONT_SIZE_CSS = f"""
<style>
h1 {{
    font-size: 36px !important;
}}
</style>
"""
st.write(FONT_SIZE_CSS, unsafe_allow_html=True)

players = pd.read_csv("players.csv")
players = players.drop_duplicates()

st.selectbox("Search for a player... ", players)
# print the selected hobby
#st.write("Your hobby is: ", hobby)
