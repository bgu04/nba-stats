import pymongo

K = 60.
HOME_ADVANTAGE = 150.

def getDBCollection(coll_name):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["nba"]
    print('DB connected')
    return db[coll_name]

def elo_pred(elo1, elo2):
    pred = (1. / (10. ** (-(elo1 - elo2) / 400.) + 1.))
    return pred

def expected_margin(elo_diff):
    return((7.5 + 0.006 * elo_diff))

def elo_update(w_elo, l_elo, margin):
    elo_diff = w_elo - l_elo
    pred = elo_pred(w_elo, l_elo)
    mult = ((margin + 3.) ** 0.8) / expected_margin(elo_diff)
    update = K * mult * (1 - pred)
    print("**", w_elo, l_elo, pred, margin, mult, update)
    return(pred, update)

elo_map = {}
pred_map = {}

seasons = ['2015']

games_coll = getDBCollection('games')

count_total = 0
count_correct = 0
count_wrong = 0

for season in seasons:

    # reset startign values
    for key in elo_map:
        elo_map[key] = (.00 * elo_map[key]) + (1.0 * 1500)
        # elo_map[key] = 1500.

    print('=================================================', season)

    cursor = games_coll.find({'seasonYear': season}).sort([('endTimeUTC', 1)])
    for g in cursor:

        hTeam_score = g['hTeam']['score']['points']
        vTeam_score = g['vTeam']['score']['points']

        if hTeam_score == '' or vTeam_score == '':
            continue

        if int(hTeam_score) > int(vTeam_score):
            home_win = True
        else:
            home_win = False

        print(g['endTimeUTC'], g['vTeam']['shortName'], g['vTeam']['score']['points'], 
            g['hTeam']['shortName'], g['hTeam']['score']['points'], home_win)

        hTeam_name = g['hTeam']['shortName']
        vTeam_name = g['vTeam']['shortName']

        if hTeam_name in elo_map:
            h_elo = float(elo_map[ hTeam_name ])
        else:
            h_elo = 1500.

        if vTeam_name in elo_map:
            v_elo = float(elo_map[ vTeam_name ])
        else:
            v_elo = 1500. 

        margin = abs(float(vTeam_score) - float(hTeam_score))

        h_elo += HOME_ADVANTAGE

        if home_win:
            pred, update = elo_update(h_elo, v_elo, margin)
            h_elo += update
            v_elo -= update
        else:
            pred, update = elo_update(v_elo, h_elo, margin)
            h_elo -= update
            v_elo += update
        
        # update map
        elo_map[ hTeam_name ] = h_elo
        elo_map[ vTeam_name ] = v_elo

        count_total += 1
        if (home_win and pred > 0.5) or (not home_win and pred < 0.5):
            count_correct += 1
            print('--', home_win, v_elo, h_elo, pred, 'Correct')
        else:
            count_wrong += 1
            print('--', home_win, v_elo, h_elo, pred, 'Wrong')

        # update DB
        games_coll.update_one( { '_id': g['_id'] } , 
            { "$set": {'elo_pred': pred, 'hTeam.elo': h_elo,  'vTeam.elo': v_elo}  } )


print('total: ', count_total, ' correct:', count_correct, ' wrong:',  count_wrong, ' %', float(count_correct/count_total))