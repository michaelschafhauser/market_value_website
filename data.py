import requests
import json
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
import os
import io
from PIL import Image

load_dotenv()
headers = CaseInsensitiveDict()
headers["accept"] = "application/json"
headers["X-AUTH-TOKEN"] = os.getenv("AUTH-TOKEN")
headers["Content-Type"] = "application/json"


URL1 = 'https://market-value-api-om3gdzslta-ew.a.run.app/predict'
URL2 = "https://futdb.app/api/players/search"
URL4 = "https://futdb.app/api/leagues/"


def get_player_data(requested_player):
    params_url1 = {'player_name': requested_player}
    # get the data from our prediction api
    prediction_data = requests.get(URL1, params=params_url1)
    data = prediction_data.json()
    return data

def get_futdb_data(requested_player):
    params_url2 = {'name': requested_player}
    api_call = json.dumps(params_url2)
    resp = requests.post(URL2, headers=headers, data=api_call).json()
    return resp['items'][0]


def get_player_id(player_name):
    url = "https://futdb.app/api/players/search"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["X-AUTH-TOKEN"] = os.getenv("AUTH-TOKEN")
    headers["Content-Type"] = "application/json"

    api_call = {"name": player_name}

    data = json.dumps(api_call)

    resp = requests.post(url, headers=headers, data=data)

    if resp.json()["items"]:

        temp_list = []
        for i in range(resp.json()["count"]):
            temp_list.append(resp.json()["items"][i]["resource_base_id"])
        num_of_players = len(set(temp_list))

        player_base_id = temp_list[0]

        temp_list = []
        for j in range(resp.json()["count"]):
            temp_list.append(resp.json()["items"][j]["resource_id"])
        card_index = temp_list.index(player_base_id)

        player_dict = resp.json()["items"][card_index]

        if num_of_players > 1:
            return None

        else:
            return player_dict["id"]
    else:
        return None


def get_player_image(player_id):
    url = "https://futdb.app/api/players/"

    headers = CaseInsensitiveDict()
    headers["accept"] = "*/*"
    headers["X-AUTH-TOKEN"] = os.getenv("AUTH-TOKEN")

    response = requests.get(url + str(player_id) + "/image", headers=headers)

    in_memory_file = io.BytesIO(response.content)

    im = Image.open(in_memory_file)

    pic_path = "image/player_image.png"
    im.save(pic_path)

    return pic_path
