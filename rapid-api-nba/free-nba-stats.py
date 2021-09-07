import requests
import pymongo
from time import sleep

def getDBCollection():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db["stats"]

URL = "https://free-nba.p.rapidapi.com/stats"

nba_headers = {
    'x-rapidapi-key': "19a63d465cmsh92e850cca87e110p146292jsn6980365e4b59",
    'x-rapidapi-host': 'free-nba.p.rapidapi.com'
}

def callRapidAPI(page):
    response = requests.get(
        URL,
        params = { 'page': page, 'per_page': 100 }, 
        headers = nba_headers
    )
    return response.json()['data']

stats_coll = getDBCollection()

for i in range(10530, 11460):
    try:
        stats =  callRapidAPI(i)
    except:
        print('Oops, need to wait a bit to continue ...')
        sleep(20)
        stats =  callRapidAPI(i)

    dup_count = 0
    for stat in stats:
        if stats_coll.find_one({"id": stat["id"]}):
            dup_count += 1
        else:
            stats_coll.insert_one(stat)
    if dup_count > 0:
        print('found dups, ignored ', dup_count)
    if i % 100 == 0:
        print('Collected at page: ', i)
        sleep(30)
    elif i % 10 == 0:
        print('Collected at page: ', i)
        sleep(10)
    
