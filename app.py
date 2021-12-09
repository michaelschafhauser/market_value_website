import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from data import get_player_data, get_futdb_data, get_player_id, get_player_image
import requests
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
import os
from dict_country_club import country_dict, club_dict
from PIL import Image

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
# futdb name search URL ==========================
searched_player = get_futdb_data(player)

if data['prediction'][:3] == 'EUR' :


    """
    # 🎉 Player estimated Value 🎉
    """
    # player predicted value =======================
    st.markdown(f"<h1 style='text-align: center;\
                color: red;'>{data['prediction']} 💸</h1>",unsafe_allow_html=True)


    stats_columns = st.columns(2)
    # player image =================================
    pic_path = get_player_image(get_player_id(player))
    image = Image.open(pic_path)
    stats_columns[0].image(image, use_column_width=False)
    stats_columns[0].write(f"Overall Rating {data['features']['overall'][0]} ⭐")
    # st.metric("Player name", searched_player['name'])


    # Player Stats DF ============================================
    list_of_stats = ['name', 'age', 'height', 'weight']
    stats_dictionary = {}
    for stat in list_of_stats:
        stats_dictionary[stat] = str(searched_player[stat])

    league_ref = searched_player["league"]
    nation_ref = searched_player["nation"]
    club_ref = searched_player["club"]

    for i in range(len(country_dict)):
        if nation_ref == country_dict[i]["id"]:
            stats_dictionary["Nationality"] = (country_dict[i]["name"])


    params_url4 = {'id': league_ref}
    league_resp = requests.get(URL4, params=params_url4, headers=headers).json()
    league_name = league_resp['items']
    for i in range(len(league_name)):
        if league_ref == league_name[i]["id"]:
            stats_dictionary["League"] = (league_name[i]["name"])


    for i in range(len(club_dict)):
        if league_ref == club_dict[i]["league"] and club_ref == club_dict[i]["id"]:
            stats_dictionary["Club"] = (club_dict[i]["name"])


    @st.cache
    def get_player_stats():
        return pd.DataFrame.from_dict(stats_dictionary, orient='index', columns=['Player Stats'])


    stats_df = get_player_stats()

    stats_df = stats_df.rename({
        "age": "Age",
        "height": "Height (cm)",
        "weight": "Weight (kg)"
    })
    stats_columns[1].table(stats_df)
    # ====================================================================

    @st.cache
    def get_dataframe_data():
        return pd.DataFrame.from_dict(data['features'])


    # RADAR CHART =======================================================
    def generate_radar_chart():
        r=[]
        theta = []
        for key, value in data['features'].items():
            if key != 'overall':
                r.append(value[0])
                theta.append(key)

        df = pd.DataFrame(dict(r=r, theta=theta))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        return fig

    '''
    # Player Attributes
    '''
    df = get_dataframe_data()
    df.drop(columns=['overall'], inplace=True)
    hdf = df.assign(hack='').set_index('hack')
    st.table(hdf)

    radar = generate_radar_chart()
    st.write(radar)



else:
    """
    # Uups 🤷🏼‍♂️
    """
