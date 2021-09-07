from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS
from dateutil import parser
from bson.objectid import ObjectId
import time


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'nba'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/nba'

mongo = PyMongo(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/teams', methods=['GET'])
def get_all_teams():
    teams = mongo.db.teams_standard
    output = []
    for s in teams.find({"$or": [{"leagues.standard.confName": "East"}, {"leagues.standard.confName": "West"}]}):
        s['_id'] = str(s['_id'])
        output.append(s)
    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/api/teams/<string:teamId>', methods=['GET'])
def get_players_by_team(teamId):
    players = mongo.db.players_standard
    output = []
    for s in players.find({"$and": [{"teamId": teamId}, {"leagues.standard.active": "1"}]}):
        s['_id'] = str(s['_id'])
        output.append(s)
    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/players/<string:playerId>', methods=['GET'])
def get_players_by_id(playerId):
    players = mongo.db.players_standard
    s = players.find_one({"playerId": playerId})
    s['_id'] = str(s['_id'])
    response = jsonify(s)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/players/summary/<string:year>', methods=['GET'])
def get_players_summary_by_year(year):
    players = mongo.db.espn_player_stats
    output = []
    for s in players.find({"seasonYear": year}):
        s['_id'] = str(s['_id'])
        output.append(s)
    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/stats/<string:playerId>', methods=['GET'])
def get_stats_by_player(playerId):
    stats = mongo.db.stats_standard
    output = []
    for s in stats.find({"playerId": playerId}).sort([('endTimeUTC', -1)]):
        # print(s)
        gameTime = parser.parse(s['startTimeUTC'])
        output.append({
            'playerName': s['playerName'],
            'teamId': s['teamId'],
            'teamName': s['teamName'],
            'gameId': s['gameId'],
            'date': gameTime.strftime('%m/%d/%Y'),
            'pos': s['pos'],
            'points': s['points'],
            'min': s['min'],
            'fgm': s['fgm'],
            'fga': s['fga'],
            'fgp': s['fgp'],
            'ftm': s['ftm'],
            'fta': s['fta'],
            'ftp':s['ftp'],
            'tpm':s['tpm'],
            'tpa':s['tpa'],
            'tpp':s['tpp'],
            'offReb':s['offReb'],
            'defReb':s['defReb'],
            'totReb':s['totReb'],
            'assists':s['assists'],
            'pFouls':s['pFouls'],
            'steals':s['steals'],
            'turnovers':s['turnovers'],
            'blocks':s['blocks'],
            'plusMinus':s['plusMinus']
        })
    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/api/game-stats/<string:gameId>', methods=['GET'])
def get_stats_by_game(gameId):
    stats = mongo.db.stats_games
    output = []
    for s in stats.find({"gameId": gameId}):
        # print(s)
        output.append({
            'teamId': s['teamId'],
            'gameId': s['gameId'],
            'fastBreakPoints': s['fastBreakPoints'],
            'pointsInPaint': s['pointsInPaint'],
            'secondChancePoints': s['secondChancePoints'],
            'pointsOffTurnovers': s['pointsOffTurnovers'],
            'biggestLead': s['biggestLead'],
            'points': s['points'],
            'longestRun': s['longestRun'],
            'min': s['min'],
            'fgm': s['fgm'],
            'fga': s['fga'],
            'fgp': s['fgp'],
            'ftm': s['ftm'],
            'fta': s['fta'],
            'ftp':s['ftp'],
            'tpm':s['tpm'],
            'tpa':s['tpa'],
            'tpp':s['tpp'],
            'offReb':s['offReb'],
            'defReb':s['defReb'],
            'totReb':s['totReb'],
            'assists':s['assists'],
            'pFouls':s['pFouls'],
            'steals':s['steals'],
            'turnovers':s['turnovers'],
            'blocks':s['blocks'],
            'plusMinus':s['plusMinus']
        })

    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")
    
    return response


@app.route('/api/games/<string:gameId>', methods=['GET'])
def get_game_by_id(gameId):
    games = mongo.db.games
    output = []
    for s in games.find({"gameId": gameId}):
        s['_id'] = str(s['_id'])
        output.append(s)

    response = jsonify(output[0])
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.route('/api/games', methods=['GET'])
def get_latest_games():
    games = mongo.db.games
    output = []
    for s in games.find({}).sort([('endTimeUTC', -1)]).limit(100):
        s['_id'] = str(s['_id'])
        output.append(s)

    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.route('/api/salaries/<string:year>', methods=['GET'])
def get_salaries_by_year(year):
    salaries = mongo.db.nba_salaries
    output = []
    for s in salaries.find({'season': year}):
        s['_id'] = str(s['_id'])
        output.append(s)

    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route('/api/topsalaries', methods=['GET'])
def get_top_salaries():
    salaries = mongo.db.nba_salaries
    output = []
    for s in salaries.find({'rank': "1"}).sort([('season', 1)]):
        s['_id'] = str(s['_id'])
        output.append(s)

    response = jsonify(output)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response



@app.route('/api/player-stats/<string:gameId>', methods=['GET'])
def get_player_stats_by_game(gameId):
    stats = mongo.db.stats_standard
    output = []
    for s in stats.find({"gameId": gameId}):
        s['_id'] = str(s['_id'])
        output.append(s)

    response = jsonify(sorted(output, key=lambda x: int(x['points']), reverse=True))
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.route("/api/message", methods=['POST'])
def setMessage():
    posted_data = request.get_json()
    msg_coll = mongo.db.site_messages
    posted_data['timestamp'] = time.strftime('%A %B, %d %Y %H:%M:%S')
    msg_coll.insert_one(posted_data)
    print('---', posted_data)
    return jsonify(str("Successfully stored  " + str(posted_data)))

@app.route('/api/chart', methods=['GET'])
def get_chart():
    
    chart_data = {
    height: 250,
    type: 'area',
    options: {
        dataLabels: {
            enabled: true
        },
        stroke: {
            width: 2,
            curve: 'smooth'
        },
        colors: ['#ff5252', '#4680ff'],
        fill: {
            type: 'solid',
            opacity: 0.2
        },
        markers: {
            size: 3,
            opacity: 0.9,
            colors: '#fff',
            strokeColor: ['#ff5252', '#4680ff'],
            strokeWidth: 2,
            hover: {
                size: 7
            }
        },
        xaxis: {
            type: 'datetime',
            categories: ['2019-01-19', '2019-02-19', '2019-03-19', '2019-04-19', '2019-05-19', '2019-06-19', '2019-07-19']
        },
        tooltip: {
            x: {
                format: 'dd/MM/yy HH:mm'
            }
        }
    },
    series: [
        {
            name: 'Expense',
            data: [40, 75, 20, 45, 30, 50, 30]
        },
        {
            name: 'Income',
            data: [90, 40, 60, 20, 10, 0, 0]
        }
    ]
    }

    response = jsonify(chart_data)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response



if __name__ == '__main__':
    app.run(debug=True)