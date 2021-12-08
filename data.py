import requests
import json
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
import os

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
