import requests
import pymongo
from time import sleep

def getDBCollection():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db["games"]

URL = "https://api-nba-v1.p.rapidapi.com/games/seasonYear/2013"

nba_headers = {
    'x-rapidapi-key': '19a63d465cmsh92e850cca87e110p146292jsn6980365e4b59',
    'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com'
}

def callRapidAPI():
    response = requests.get(
        URL,
        headers = nba_headers
    )
    # print(response.json())
    return response.json() 

games_coll = getDBCollection()
data = callRapidAPI()

game_groups = data['api']['games']

count = 0
for game in game_groups:
    games_coll.insert_one(game)
    count += 1
    if count % 10 == 0:
        print(count)

print('Total games: ', count)