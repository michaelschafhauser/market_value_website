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
    # Player estimated value
    """
    # player predicted value =======================
    st.markdown(f"<h1 style='text-align: center;\
                '>💸 {data['prediction']} 💸</h1>"                                                                                                                                                                                                ,
                unsafe_allow_html=True)


    stats_columns = st.columns(2)
    # player image =================================
    pic_path = get_player_image(get_player_id(player))
    image = Image.open(pic_path)
    stats_columns[0].image(image, use_column_width=False)
    stats_columns[0].subheader(f"⭐ Rating: {data['features']['overall'][0]} ⭐")
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


    if len(data["transfer_history"]) == 1:
        stats_dictionary["Nº Clubs"] = str(1)
    else:
        stats_dictionary["Nº Clubs"] = str(len(set(data["transfer_history"]["receiving_club"])))


    @st.cache
    def get_player_stats():
        return pd.DataFrame.from_dict(stats_dictionary, orient='index', columns=['Player stats'])


    stats_df = get_player_stats()

    stats_df = stats_df.rename({
        "age": "Age",
        "height": "Height (cm)",
        "weight": "Weight (kg)",
        "name": "Name"
    })

    stats_columns[1].table(stats_df)
    # ====================================================================

    @st.cache
    def get_dataframe_data():
        df = pd.DataFrame.from_dict(data['features'])
        df.drop(columns=['overall'], inplace=True)
        df = df.rename(columns={
            "pace": "Pace",
            "shooting": "Shooting",
            "passing": "Passing",
            "dribbling": "Dribbling",
            "defending": "Defending",
            "physic": "Physical"
            })
        return df


    # RADAR CHART =======================================================
    def generate_radar_chart():
        r=[]
        theta = []
        for key, value in data['features'].items():
            if key != 'overall':
                r.append(value[0])
                theta.append(key)

        theta = ['Pace', 'Shooting', 'Passing', 'Dribbling','Defending', 'Physical']

        df = pd.DataFrame(dict(r=r, theta=theta))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        return fig

    '''
    # Player attributes
    '''
    df = get_dataframe_data()
    hdf = df.assign(hack='').set_index('hack')
    st.table(hdf)

    radar = generate_radar_chart()
    st.write(radar)

    # TRANSFER HISTORY =====================================================
    if len(data['transfer_history']) != 1:
        transfer_fee_values=[]
        for i in range(len(data["transfer_history"]["transfer_fee"])):
            transfer_fee_values.append(round(data["transfer_history"]["transfer_fee"][i],1))

        transfer_fee_years=[]
        for i in range(len(data["transfer_history"]["season"])):
            transfer_fee_years.append(data["transfer_history"]["season"][i])

        transfer_age=[]
        for i in range(len(data["transfer_history"]["age"])):
            transfer_age.append(round(data["transfer_history"]["age"][i]))

        receiving_club = []
        for i in range(len(data["transfer_history"]["receiving_club"])):
            receiving_club.append(data["transfer_history"]["receiving_club"][i])


        df_transfer_values = pd.DataFrame(transfer_fee_values)
        df_transfer_values = df_transfer_values.rename(columns={0: 'Transfer_Values'})

        df_transfer_years = pd.DataFrame(transfer_fee_years)
        df_transfer_years = df_transfer_years.rename(columns={0: 'Transfer_Years'})
        df_transfer_years["Transfer_Years"]=df_transfer_years["Transfer_Years"].apply(lambda x : int(x[:4]))

        df_transfer_age = pd.DataFrame(transfer_age)
        df_transfer_age = df_transfer_age.rename(columns={0: 'Age'})

        df_receiving_club = pd.DataFrame(receiving_club)
        df_receiving_club = df_receiving_club.rename(columns={0: 'Receiving Club'})


        df_all = pd.concat([df_transfer_years, df_transfer_values,df_transfer_age, df_receiving_club], axis=1)
        n_of_digits = sum(c.isdigit() for c in data["prediction"])-1
        age_counter = 2021 - df_all.Transfer_Years.iloc[-1]
        df_all.loc[len(df_all.index)] = [
            2022,
            int(data['prediction'][4:4 + n_of_digits]),
            df_all.Age.iloc[-1]+age_counter,
            "-"
        ]

        '''
        # Transfer history
        '''

        df_all

        fig = px.area(
        df_all,
        x='Transfer_Years',
        y="Transfer_Values",
        range_x=[df_all['Transfer_Years'].min()-1, df_all['Transfer_Years'].max()+1]
        )
        st.plotly_chart(fig)

    else:
        '''
        # No transfer information
        '''







else:
    """
    # Uups 🤷🏼‍♂️
    """
