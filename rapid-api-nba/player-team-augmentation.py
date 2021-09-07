import pymongo
from time import sleep

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]

teams_coll = getDBCollection('teams_standard')
players_coll = getDBCollection('players_standard')

team_map = {}
count = 0
for team in teams_coll.find({}):
    print(team)
    team_map[team['teamId']] = team['fullName']

print('---', len(team_map))

cursor = players_coll.find({})
for data in cursor:
    try:
        players_coll.update_one( { '_id': data['_id'] } , { "$set": { 'teamName': team_map[data['teamId']] } } )
        print('Updated ', data['_id'])
    except: 
        continue

print ('Done')