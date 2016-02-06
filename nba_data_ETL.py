__author__ = 'shane'
import requests
import json
import cPickle as pickle
from pyquery import PyQuery as pyq
import re
import datetime
NBA_event_2015 = pickle.load(open('C:/Users/shane/PycharmProjects/NBA_bet_odds/NBA_event_2015', "r" ))
result_2015 = pickle.load(open('C:/Users/shane/PycharmProjects/NBA_bet_odds/result_2015', "r" ))
conf = {u'Atlanta Hawks': 'E',
 u'Boston Celtics': 'E',
 u'Brooklyn Nets': 'E',
 u'Charlotte Hornets': 'E',
 u'Chicago Bulls': 'E',
 u'Cleveland Cavaliers': 'E',
 u'Dallas Mavericks': 'W',
 u'Denver Nuggets': 'W',
 u'Detroit Pistons': 'E',
 u'Golden State Warriors': 'W',
 u'Houston Rockets': 'W',
 u'Indiana Pacers': 'E',
 u'Los Angeles Clippers': 'W',
 u'Los Angeles Lakers': 'W',
 u'Memphis Grizzlies': 'W',
 u'Miami Heat': 'E',
 u'Milwaukee Bucks': 'E',
 u'Minnesota Timberwolves': 'W',
 u'New Orleans Pelicans': 'W',
 u'New York Knicks': 'E',
 u'Oklahoma City Thunder': 'W',
 u'Orlando Magic': 'E',
 u'Philadelphia 76ers': 'E',
 u'Phoenix Suns': 'W',
 u'Portland Trail Blazers': 'W',
 u'Sacramento Kings': 'W',
 u'San Antonio Spurs': 'W',
 u'Toronto Raptors': 'E',
 u'Utah Jazz': 'W',
 u'Washington Wizards': 'E'}

under_over_list = []
for i in NBA_event_2015:
    if filter(lambda x: x['home_team'] == i['home_team'] and x['away_team'] == i['away_team'] and
                 x['start_time'].split()[0].replace('-', '') == i['event_date'], result_2015):

        i['total_score'] = int(i['home_score']) + int(i['away_score'])
        i['away_conf'] = conf[i['away_team']]
        i['home_conf'] = conf[i['home_team']]
        i['away_winning_percent'] = float(int(i['away_standing'].split('-')[0]))/float(int(i['away_standing'].split('-')[0]) + int(i['away_standing'].split('-')[1]))
        i['home_winning_percent'] = float(int(i['home_standing'].split('-')[0]))/float(int(i['home_standing'].split('-')[0]) + int(i['home_standing'].split('-')[1]))

        over_under = filter(lambda x: x['home_team'] == i['home_team'] and x['away_team'] == i['away_team'] and
                 x['start_time'].split()[0].replace('-', '') == i['event_date'], result_2015)[0]['over_under']
        i['weekday'] = datetime.datetime.strptime(i['event_date'], "%Y%m%d").date().strftime("%A")
        i.update({'over_under': over_under})
        if i['over_under']:
            if i['total_score'] >= float(i['over_under']):
                i['over_under_result'] = 'over'
            else:
                i['over_under_result'] = 'under'
            under_over_list.append(i)

json.dump(under_over_list, open('C:/Users/shane/PycharmProjects/NBA_bet_odds/nba_ETL_result_2015.json', "wb" ))