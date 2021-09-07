import requests
import pymongo
from time import sleep

def getDBCollection(coll_name):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll_name]

URL = "https://free-nba.p.rapidapi.com/players"

nba_headers = {
    'x-rapidapi-key': 'f6001cd7demsh8ba79a5c5fc120bp180fd8jsn35b15f301fc6',
    'x-rapidapi-host': 'free-nba.p.rapidapi.com'
}

def callRapidAPI(page, api_url):
    response = requests.get(
        api_url,
        params = { 'page': page,  'per_page': 100 },
        headers = nba_headers
    )
    return response.json()['data']


players_coll = getDBCollection("players")



for i in range(36):
    dup_count = 0
    for player in callRapidAPI(i, URL):
        if players_coll.find_one({"id": player["id"]}):
            dup_count += 1
        else:
            players_coll.insert_one(player)
    print('finished page: ', i)
    sleep(2)