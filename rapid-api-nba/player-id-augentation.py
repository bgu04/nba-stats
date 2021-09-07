import pymongo

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]


players_coll = getDBCollection('players_standard')
salaries_coll = getDBCollection('nba_salaries')
espn_player_stats_coll = getDBCollection('espn_player_stats')

"""
for s in salaries_coll.find({}):
    firstName = s["firstName"]
    lastName = s["lastName"]
    try:
        player = players_coll.find_one({ "$and": [{"firstName": firstName }, {"lastName": lastName }] })
        salaries_coll.update_one( { '_id': s['_id'] } , { "$set": { 'playerId': player['playerId'] } } )
        print("updated")
    except:
        print("----- Cannot find player", firstName, lastName)


for s in espn_player_stats_coll.find({}):
    firstName = s["firstName"]
    lastName = s["lastName"]
    try:
        player = players_coll.find_one({ "$and": [{"firstName": firstName }, {"lastName": lastName }] })
        espn_player_stats_coll.update_one( { '_id': s['_id'] } , { "$set": { 'playerId': player['playerId'] } } )
        print("espn updated")
    except:
        print("----- Cannot find player in ESPN", firstName, lastName)
"""

for s in salaries_coll.find({"season": "2022"}):
    key = s.get("playerId", None)
    if key is None:
        continue
    else:
        try:
            players_coll.update_one( { 'playerId': key } , { "$set": { 'recentSalary': s['salary'] } } )
            print("updated", s['firstName'], s['lastName'])
        except:
            print("----- Cannot find player", s['firstName'], s['lastName'], key)