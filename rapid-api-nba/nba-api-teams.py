import requests
import pymongo
from time import sleep

def getDBCollection():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db["teams_standard"]

URL = "https://api-nba-v1.p.rapidapi.com/teams/league/standard"

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

teams_coll = getDBCollection()
data = callRapidAPI()

team_groups = data['api']['teams']

count = 0
for team in team_groups:
    teams_coll.insert_one(team)
    count += 1
    if count % 10 == 0:
        print(count)

print('Total teams: ', count)