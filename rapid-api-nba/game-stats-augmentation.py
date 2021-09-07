import pymongo
from time import sleep

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]

games_coll = getDBCollection('games')
stats_coll = getDBCollection('stats_standard')

stats_cursor = stats_coll.find({})
for stat in stats_cursor:

    game = games_coll.find_one({'gameId': stat['gameId']})
    print('- game found')
    try:
        stats_coll.update_one( { '_id': stat['_id'] } , { "$set": {'endTimeUTC': game['endTimeUTC'], 'startTimeUTC': game['startTimeUTC'], 'city': game['city'] } } )
        print('Updated ', stat['_id'])
    except: 
        continue
