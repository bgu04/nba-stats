"""
This program collects NBA salary data from ESPN for one season. 
Update season value in order to collect data for different year.
- Ben
"""

import requests
from bs4 import BeautifulSoup
import pymongo
import re

salary_list = []

def getDBCollection(coll):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll]

def parseTrs(elements):
    for element in elements:
        tds = element.find_all("td")
        s = {}
        s['rank'] = tds[0].text
        if s['rank'] == 'RK':
            continue
        nametokens = re.split(' |, ',  tds[1].text)
        # print(nametokens)

        s['firstName'] = nametokens[0]
        s['lastName'] = nametokens[1]
        s['pos'] = nametokens[2]
        s['team'] = tds[2].text
        s['salary'] = tds[3].text
        salary_list.append(s)

salaries_coll = getDBCollection('nba_salaries')

season = '2020'

for i in range(1, 11):
    URL = "http://www.espn.com/nba/salaries/_/year/" + season + "/page/" + str(i) + "/seasontype/4"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="my-players-table")
    elements = results.find_all("tr")
    parseTrs(elements)
    print ('done ', i)

for s in salary_list:
    s['season'] = season
    salaries_coll.insert_one(s)

print('data inserted')