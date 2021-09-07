import requests
import pymongo
from time import sleep

def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[collName]

URL = "https://api-nba-v1.p.rapidapi.com/statistics/players/playerId/"

nba_headers = {
    'x-rapidapi-key': '19a63d465cmsh92e850cca87e110p146292jsn6980365e4b59',
    'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com'
}

def callRapidAPI(playerId):
    response = requests.get(
        URL + playerId,
        headers = nba_headers
    )
    # print(response.json())
    return response.json() 

players_coll = getDBCollection("players_standard")
stats_coll = getDBCollection("stats_standard")

limit = 0
for player in players_coll.find():
    print(player)

    if stats_coll.find_one({"playerId": player["playerId"]}):
        print('Already fetched for player ',  player["playerId"])
        continue
    else:
        data = callRapidAPI(player["playerId"])

        count = 0
        for stat in data['api']["statistics"]:
            stats_coll.insert_one(stat)
            count += 1

        limit += 1
        print(limit, 'Inserted ', count, ' records for ', player["playerId"])

        #if limit % 30 == 0:
        #    sleep(30)