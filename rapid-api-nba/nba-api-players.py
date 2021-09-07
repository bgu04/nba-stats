import requests
import pymongo
from time import sleep

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]

URL = "https://api-nba-v1.p.rapidapi.com/players/league/standard"

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

players_coll = getDBCollection("players_standard")

teams_coll = getDBCollection('teams_standard')
team_map = {}
count = 0
for team in teams_coll.find({}):
    print(team)
    team_map[team['teamId']] = team['fullName']

data = callRapidAPI()
player_groups = data['api']['players']

count = 0
for player in player_groups:
    if player is None or player["firstName"] is None:
        continue
    exist = players_coll.find_one({ "$and": [{"firstName": player["firstName"] }, {"lastName": player["lastName"] }] })
    if exist is None:
        players_coll.insert_one(player)
        print('inserted ', player)
    else:
        if exist["teamId"] == player["teamId"]:
            continue
        players_coll.update_one( { '_id': exist['_id'] } , 
            { "$set": { 
                    'teamId': player['teamId'],
                    'teamName': team_map[player['teamId']],
                    'leagues.standard.jersey': player['leagues']['standard']['jersey']
                } 
            } 
        )
        print('updated ', player['playerId'], player['firstName'], player['lastName'])
    count += 1
    if count % 10 == 0:
        print(count)

print('Total players: ', count)


