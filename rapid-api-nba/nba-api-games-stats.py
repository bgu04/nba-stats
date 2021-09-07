import requests
import pymongo
from time import sleep

def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[collName]

URL = "https://api-nba-v1.p.rapidapi.com/statistics/games/gameId/"

nba_headers = {
    'x-rapidapi-key': '19a63d465cmsh92e850cca87e110p146292jsn6980365e4b59',
    'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com'
}

def callRapidAPI(id):
    response = requests.get(
        URL + id,
        headers = nba_headers
    )
    # print(response.json())
    return response.json() 

games_coll = getDBCollection("games")
stats_coll = getDBCollection("stats_games")

limit = 0
for game in games_coll.find({"seasonYear" : "2015"}):
    # print(game)

    if stats_coll.find_one({"gameId" : game["gameId"]}):
        print('Already fetched for game ',  game["gameId"])
        continue
    else:
        data = callRapidAPI(game["gameId"])

        count = 0
        for stat in data['api']["statistics"]:
            print(stat)
            stats_coll.insert_one(stat)
            count += 1

        limit += 1
        print(limit, 'Inserted ', count, ' records for ', game["gameId"])