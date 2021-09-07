import pymongo
from time import sleep

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]

players_coll = getDBCollection('players_standard')
stats_coll = getDBCollection('stats_standard')

players_map = {}
count = 0
for p in players_coll.find({}):
    players_map[p['playerId']] = p['firstName'] + ' ' + p['lastName']

print('---', len(players_map))

stats_cursor = stats_coll.find({})
for stat in stats_cursor:
    try:
        stats_coll.update_one( { '_id': stat['_id'] } , { "$set": { 'playerName': players_map[stat['playerId']] } } )
        print('Updated ', stat['_id'])
    except: 
        continue

print('Total teams: ', count)