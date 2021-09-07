import requests
import pymongo
from time import sleep

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]

teams_coll = getDBCollection('teams_standard')
stats_coll = getDBCollection('stats_standard')

team_map = {}
count = 0
for team in teams_coll.find({}):
    print(team)
    team_map[team['teamId']] = team['fullName']

print('---', len(team_map))

stats_cursor = stats_coll.find({})
for stat in stats_cursor:
    try:
        stats_coll.update_one( { '_id': stat['_id'] } , { "$set": { 'teamName': team_map[stat['teamId']] } } )
        print('Updated ', stat['_id'])
    except: 
        continue

print('Total teams: ', count)