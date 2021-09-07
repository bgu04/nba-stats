import requests
import pymongo
from time import sleep


def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[collName]

URL = "https://api-nba-v1.p.rapidapi.com/gameDetails/"

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

cursor = games_coll.find({"officials": {"$exists": False} })
for game in cursor:

    try:
        detail_json = callRapidAPI(game["gameId"])
        game_detail = detail_json["api"]["game"][0]
        print("updating ", game['gameId'], game_detail["officials"])
        games_coll.update_one( { '_id': game['_id'] } , { "$set": {'officials': game_detail["officials"]} } )
    except:
        print('got error getting data: ', game["gameId"])
        continue


