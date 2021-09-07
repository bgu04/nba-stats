import requests
import csv

URL = "https://free-nba.p.rapidapi.com/teams"

nba_headers = {
    'x-rapidapi-key': 'f6001cd7demsh8ba79a5c5fc120bp180fd8jsn35b15f301fc6',
    'x-rapidapi-host': 'free-nba.p.rapidapi.com'
}

params = { 'page': '0' }

response = requests.get(
    "https://free-nba.p.rapidapi.com/teams",
    params = { 'page': '0' }, 
    headers = nba_headers
)

json_response = response.json()

f_teams = csv.writer(open("teams.csv", "w"))

f_teams.writerow(["id", "abbreviation", "city", "conference", "division", "full_name", "name"])

for team in json_response['data']:
    f_teams.writerow([
        team["id"], 
        team["abbreviation"],
        team["city"],
        team["conference"],
        team["division"],
        team["full_name"],
        team["name"]
    ])

print('Done')