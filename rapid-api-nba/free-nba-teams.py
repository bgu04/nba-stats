import requests
import pymongo
from time import sleep

def getDBCollection(coll_name):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll_name]

URL = "https://free-nba.p.rapidapi.com/teams"

nba_headers = {
    'x-rapidapi-key': 'f6001cd7demsh8ba79a5c5fc120bp180fd8jsn35b15f301fc6',
    'x-rapidapi-host': 'free-nba.p.rapidapi.com'
}

def callRapidAPI(page, api_url):
    response = requests.get(
        api_url,
        params = { 'page': page },
        headers = nba_headers
    )
    return response.json()['data']

teams_coll = getDBCollection("teams")

for team in callRapidAPI(0, URL):
    teams_coll.insert_one(team)
