"""
This file collects yearly summary data for each player of a season from ESPN.
Update value of year to collect different season. 
- Ben
"""

import requests
import pymongo

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]

espn_stats_coll = getDBCollection('espn_player_stats')
year = '2022'
post = ''
count = 0
for i in range(1, 12):

    URL = "http://site.api.espn.com:80/apis/common/v3/sports/basketball/nba/statistics/byathlete?contentorigin=espn&isqualified=true&lang=en&region=us&season=" + year + "&seasontype=2&sort=offensive.avgPoints%3Adesc&limit=50&page=" + str(i)

    response = requests.get(URL)

    players = response.json()['athletes']

    for p in players:
        it = {}
        it['seasonYear'] = year + post
        if 'athlete' in p.keys() == False:
            continue

        it['firstName'] = p['athlete']['firstName']
        it['lastName'] = p['athlete']['lastName']
        if 'debutYear' in p['athlete'].keys():
            it['debutYear'] = p['athlete']['debutYear']
        it['position'] = p['athlete']['position']['abbreviation']
        it['age'] = p['athlete']['age']
        totals = p['categories']
        it['GP'] = totals[0]['totals'][0]
        it['MIN'] = totals[0]['totals'][1]
        it['PTS'] = totals[1]['totals'][0]
        it['FGM'] = totals[1]['totals'][1]
        it['FGA'] = totals[1]['totals'][2]
        it['FG%'] = totals[1]['totals'][3]
        it['3PM'] = totals[1]['totals'][4]
        it['3PA'] = totals[1]['totals'][5]
        it['3P%'] = totals[1]['totals'][6]
        it['FTM'] = totals[1]['totals'][7]
        it['FTA'] = totals[1]['totals'][8]
        it['FT%'] = totals[1]['totals'][9]
        it['REB'] = totals[0]['totals'][12]
        it['AST'] = totals[1]['totals'][10]
        it['STL'] = totals[2]['totals'][0]
        it['BLK'] = totals[2]['totals'][1]
        it['TO'] = totals[1]['totals'][11]
        it['DD2'] = totals[0]['totals'][6]
        it['TD3'] = totals[0]['totals'][7]
        it['PER'] = totals[0]['totals'][8]

        #print(totals[0]['totals'])
        #print(totals[1]['totals'])
        #print(totals[2]['totals'])
        #print('-----')
        espn_stats_coll.insert_one(it)
        print(it)
        print('-----', count)
        count += 1