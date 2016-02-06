# -*- coding: utf-8 -*-
__author__ = 'shane'
import requests
import random
import cPickle as pickle
import time
import json
from pyquery import PyQuery as pyq
import re
import datetime
class NBA_betting_odds_tomorrow(object):
    def __init__(self):
        self.url = 'http://www.sportsbookreview.com/betting-odds/nba-basketball/'
        self.timeout = 10
        self.proxies = {"http": "123.204.107.38:80",
                        "https": "123.204.107.38:80",}

    def betting_odds_trans(self, odds):
        if odds.startswith('+'):
            europe_odds = 1 + float(odds.replace('+', ''))/100
            return europe_odds
        if odds.startswith('-'):
            europe_odds = 1 + 100/float(odds.replace('-', ''))
            return europe_odds
    def get_betting_odds_info_list(self):
        h = requests.get(self.url, timeout = self.timeout) #, proxies = self.proxies
        text = h.content
        pq = pyq(text)
        betting_odds_info_list = []
        startdate_html = pq('.event-holder.holder-scheduled>.eventLine.status-scheduled')
        url_html = pyq(startdate_html)('meta[itemprop=\'url\']')
        matchup_html = pyq(startdate_html)('meta[itemprop=\'name\']')
        for i in range(len(startdate_html)):
            betting_odds_info_list.append({'start_time': startdate_html.eq(i).attr('rel'),
                                       'url': url_html.eq(i).attr('content'),
                                        'away_team': matchup_html.eq(i).attr('content').split(' vs ')[0],
                                       'home_team': matchup_html.eq(i).attr('content').split(' vs ')[1]})

        return betting_odds_info_list
    def get_betting_odds(self, url):
        h = requests.get(url, timeout = self.timeout) #, proxies = self.proxies
        text = h.content
        pq = pyq(text)
        betting_odds_html = pq('.el-div.eventLine-opener>.eventLine-book-value')
        betting_odds = {}
        if betting_odds_html.eq(0).text():
            if 'PK' in betting_odds_html.eq(0).text():
                betting_odds['away_line'] = 'PK'
                betting_odds['away_line_odds'] = betting_odds_html.eq(0).text().replace('PK', '')
            else:
                betting_odds['away_line'] = re.split(r'\xa0| ', betting_odds_html.eq(0).text())[0].replace(u'\xbd','.5')
                betting_odds['away_line_odds'] = re.split(r'\xa0| ', betting_odds_html.eq(0).text())[1]
        else:
            betting_odds['away_line'] = None
            betting_odds['away_line_odds'] = None

        if betting_odds_html.eq(1).text():
            if 'PK' in betting_odds_html.eq(1).text():
                betting_odds['home_line'] = 'PK'
                betting_odds['home_line_odds'] = betting_odds_html.eq(1).text().replace('PK', '')
            else:
                betting_odds['home_line'] = re.split(r'\xa0| ', betting_odds_html.eq(1).text())[0].replace(u'\xbd','.5')
                betting_odds['home_line_odds'] = re.split(r'\xa0| ', betting_odds_html.eq(1).text())[1]

        else:
            betting_odds['home_line'] = None
            betting_odds['home_line_odds'] = None
        if betting_odds_html.eq(2).text():
            betting_odds['away_money_line_odds'] =  betting_odds_html.eq(2).text()
        else:
            betting_odds['away_money_line_odds'] = None

        if betting_odds_html.eq(3).text():
            betting_odds['home_money_line_odds'] =  betting_odds_html.eq(3).text()
        else:
            betting_odds['home_money_line_odds'] = None

        if betting_odds_html.eq(4).text():
            betting_odds['over_under'] =  re.split(r'\xa0| ', betting_odds_html.eq(4).text())[0].replace(u'\xbd','.5')
            betting_odds['over_odds'] = re.split(r'\xa0| ', betting_odds_html.eq(4).text())[1]
        else:
            betting_odds['over_under'] = None
            betting_odds['over_odds'] =  None
        if betting_odds_html.eq(5).text():
            betting_odds['under_odds'] =  re.split(r'\xa0| ', betting_odds_html.eq(5).text())[1]
        else:
            betting_odds['under_odds'] = None
        betting_odds['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        betting_odds['id'] = int(url.split('-')[-1].replace('/',''))
        #betting_odds['over_odds'] =  self.betting_odds_trans(re.split(r'\xa0| ', betting_odds_html.eq(4).text())[1])
        #betting_odds['under_odds'] =  self.betting_odds_trans(re.split(r'\xa0| ', betting_odds_html.eq(5).text())[1])
        return betting_odds
    def get_total_betting_odds_tomorrow(self):
        f = open('error.log','a')
        betting_odds_info_list = self.get_betting_odds_info_list()
        for i in betting_odds_info_list:

            try:
                print i['url']
                betting_odds = self.get_betting_odds(i['url'])
                i.update(betting_odds)
            except Exception, e:
                print i['url']
                f.write(i + '   ' + str(e) + '\n')
                print str(e)
        f.close()
        return betting_odds_info_list


class NBA_betting_odds(object):
    def __init__(self):
        self.url = 'http://www.sportsbookreview.com/betting-odds/nba-basketball/?date='
        self.proxies = {"http": "123.204.107.38:80",
                        "https": "123.204.107.38:80",}
        self.timeout = 10
    def betting_odds_trans(self, odds):
        if odds.startswith('+'):
            europe_odds = 1 + float(odds.replace('+', ''))/100
            return europe_odds
        if odds.startswith('-'):
            europe_odds = 1 + 100/float(odds.replace('-', ''))
            return europe_odds
    def get_betting_odds_info_list(self, date):
        h = requests.get(self.url + date, timeout = self.timeout) #, proxies = self.proxies
        text = h.content
        pq = pyq(text)
        betting_odds_info_list = []
        startdate_html = pq('.event-holder.holder-complete>.eventLine.status-complete')
        url_html = pyq(startdate_html)('meta[itemprop=\'url\']')
        matchup_html = pyq(startdate_html)('meta[itemprop=\'name\']')
        for i in range(len(startdate_html)):
            betting_odds_info_list.append({'start_time': startdate_html.eq(i).attr('rel'),
                                       'url': url_html.eq(i).attr('content'),
                                        'away_team': matchup_html.eq(i).attr('content').split(' vs ')[0],
                                       'home_team': matchup_html.eq(i).attr('content').split(' vs ')[1]})

        return betting_odds_info_list
    def get_betting_odds(self, url):
        h = requests.get(url, timeout = self.timeout) #, proxies = self.proxies
        text = h.content
        pq = pyq(text)
        betting_odds_html = pq('.el-div.eventLine-opener>.eventLine-book-value')
        betting_odds = {}
        if betting_odds_html.eq(0).text():
            if 'PK' in betting_odds_html.eq(0).text():
                betting_odds['away_line'] = 'PK'
                betting_odds['away_line_odds'] = betting_odds_html.eq(0).text().replace('PK', '')
            else:
                betting_odds['away_line'] = re.split(r'\xa0| ', betting_odds_html.eq(0).text())[0].replace(u'\xbd','.5')
                betting_odds['away_line_odds'] = re.split(r'\xa0| ', betting_odds_html.eq(0).text())[1]
        else:
            betting_odds['away_line'] = None
            betting_odds['away_line_odds'] = None

        if betting_odds_html.eq(1).text():
            if 'PK' in betting_odds_html.eq(1).text():
                betting_odds['home_line'] = 'PK'
                betting_odds['home_line_odds'] = betting_odds_html.eq(1).text().replace('PK', '')
            else:
                betting_odds['home_line'] = re.split(r'\xa0| ', betting_odds_html.eq(1).text())[0].replace(u'\xbd','.5')
                betting_odds['home_line_odds'] = re.split(r'\xa0| ', betting_odds_html.eq(1).text())[1]

        else:
            betting_odds['home_line'] = None
            betting_odds['home_line_odds'] = None
        if betting_odds_html.eq(2).text():
            betting_odds['away_money_line_odds'] =  betting_odds_html.eq(2).text()
        else:
            betting_odds['away_money_line_odds'] = None

        if betting_odds_html.eq(3).text():
            betting_odds['home_money_line_odds'] =  betting_odds_html.eq(3).text()
        else:
            betting_odds['home_money_line_odds'] = None

        if betting_odds_html.eq(4).text():
            betting_odds['over_under'] =  re.split(r'\xa0| ', betting_odds_html.eq(4).text())[0].replace(u'\xbd','.5')
            betting_odds['over_odds'] = re.split(r'\xa0| ', betting_odds_html.eq(4).text())[1]
        else:
            betting_odds['over_under'] = None
            betting_odds['over_odds'] =  None
        if betting_odds_html.eq(5).text():
            betting_odds['under_odds'] =  re.split(r'\xa0| ', betting_odds_html.eq(5).text())[1]
        else:
            betting_odds['under_odds'] = None
        betting_odds['id'] = int(url.split('-')[-1].replace('/',''))
        #betting_odds['over_odds'] =  self.betting_odds_trans(re.split(r'\xa0| ', betting_odds_html.eq(4).text())[1])
        #betting_odds['under_odds'] =  self.betting_odds_trans(re.split(r'\xa0| ', betting_odds_html.eq(5).text())[1])
        return betting_odds

    def get_total_betting_odds(self, date):
        betting_odds_info_list = self.get_betting_odds_info_list(date)
        for i in betting_odds_info_list:
            betting_odds = self.get_betting_odds(i['url'])
            i.update(betting_odds)
        return betting_odds_info_list

class NBA_event(object):
    def __init__(self):
        self.url = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?lang=en&region=us&calendartype=blacklist&limit=100&dates='
        self.timeout = 20
    def get_nba_event(self, date):
        h = requests.get(self.url + date)
        text = h.content
        content_dict = json.loads(text)
        event_list = []
        if len(content_dict['events']) != 0:
            for i in content_dict['events']:
                event_dict = {}
                event_dict['event_date'] = date
                event_dict['away_team'] = i['competitions'][0]['competitors'][1]['team']['displayName']
                event_dict['home_team'] = i['competitions'][0]['competitors'][0]['team']['displayName']
                event_dict['id'] = i['competitions'][0]['id']
                event_dict['away_score'] = i['competitions'][0]['competitors'][1]['score']
                event_dict['home_score'] = i['competitions'][0]['competitors'][0]['score']
                if i['competitions'][0]['competitors'][1]['records']:
                    event_dict['away_standing'] = i['competitions'][0]['competitors'][1]['records'][0]['summary']
                else:
                    event_dict['away_standing'] = None
                if i['competitions'][0]['competitors'][0]['records']:
                    event_dict['home_standing'] = i['competitions'][0]['competitors'][0]['records'][0]['summary']
                else:
                    event_dict['home_standing'] = None
                event_list.append(event_dict)
        return event_list


class playsport(object):
    def __init__(self):
        self.url = 'http://www.playsport.cc/predictgame.php?action=scale'
        self.timeout = 20
        self.allianceid = allianceid = {'NBA': '3', 'EUL': '8', 'ESP': '84', 'KBL': '92', 'BJL': '97', 'CBA': '94', 'SBL': '89'}
        self.proxies = {"http": "112.25.185.171:8000",
                        "https": "112.25.185.171:8000",}
    def basketball_betting_odds(self, league, date):
        h = requests.get(self.url + '&allianceid=' + self.allianceid[league] + '&gametime=' + date, timeout = self.timeout, proxies = self.proxies)
        text = h.content
        pq = pyq(text)
        betting_info_list = []
        for i in range(len(pq('[class*="game-set"]'))/2):
            betting_info = {}
            betting_info['date'] = date
            pq1 = pyq(pq('[class*="game-set"]').eq(2*i).html())
            pq2 = pyq(pq('[class*="game-set"]').eq(1+2*i).html())
            betting_info['id'] = pq1('.td-gameinfo>div>h3').text()
            betting_info['away_score'] = pq1('.scores').text().split(' V.S. ')[0]
            betting_info['away_team'] = pq1('.scores').next().text()
            betting_info['home_score'] = pq1('.scores').text().split(' V.S. ')[1]
            betting_info['home_team'] = pq1('tr').eq(2).text()
            if pq1('.td-bank-bet01').text():
                betting_info['away_line'] = pq1('.td-bank-bet01').text().split(' , ')[0].replace(u'客 ','')
                betting_info['away_line_odds'] = pq1('.td-bank-bet01').text().split(' , ')[1].replace(u'客 ','')
            else:
                betting_info['away_line'] = ''
                betting_info['away_line_odds'] = ''
            if pq2('.td-bank-bet01').text():
                betting_info['home_line'] = pq2('.td-bank-bet01').text().split(' , ')[0].replace(u'主 ','')
                betting_info['home_line_odds'] = pq2('.td-bank-bet01').text().split(' , ')[1].replace(u'主 ','')
            else:
                betting_info['home_line'] = ''
                betting_info['home_line_odds'] = ''
            betting_info['away_money_line_odds'] = pq1('.td-bank-bet03').text().replace(u'客 ','')
            betting_info['home_money_line_odds'] = pq2('.td-bank-bet03').text().replace(u'主 ','')
            if pq1('.td-bank-bet02').text():
                betting_info['over_under'] = pq1('.td-bank-bet02').text().split(' , ')[0].replace(u'大 ','')
                betting_info['over_odds'] = pq1('.td-bank-bet02').text().split(' , ')[1]
            else:
                betting_info['over_under'] = ''
                betting_info['over_odds'] = ''
            if pq2('.td-bank-bet02').text():
                betting_info['under_odds'] = pq2('.td-bank-bet02').text().split(' , ')[1]
            else:
                betting_info['under_odds'] = ''
            if pq1('.td-bank-bet01').text():
                betting_info['away_line_num'] = pq1('.td-bank-bet01').next().text().split(' ')[1]
            else:
                betting_info['away_line_num'] = ''
            if pq2('.td-bank-bet01').text():
                betting_info['home_line_num'] = pq2('.td-bank-bet01').next().text().split(' ')[1]
            else:
                betting_info['home_line_num'] = ''
            if pq1('.td-bank-bet03').text():
                betting_info['away_money_line_num'] = pq1('.td-bank-bet03').next().text().split(' ')[1]
            else:
                betting_info['away_money_line_num'] = ''
            if pq2('.td-bank-bet03').text():
                betting_info['home_money_line_num'] = pq2('.td-bank-bet03').next().text().split(' ')[1]
            else:
                betting_info['home_money_line_num'] = ''
            if pq1('.td-bank-bet02').text():
                betting_info['over_num'] = pq1('.td-bank-bet02').next().text().split(' ')[1]
            else:
                betting_info['over_num'] = ''
            if pq2('.td-bank-bet02').text():
                betting_info['under_num'] = pq2('.td-bank-bet02').next().text().split(' ')[1]
            else:
                betting_info['under_num'] = ''
            betting_info_list.append(betting_info)
        print repr(betting_info_list).decode('unicode-escape')
        return betting_info_list
if __name__ == '__main__':
    f = open('error.log','a')
    start_day = datetime.datetime.strptime('20151231', "%Y%m%d").date()
    numdays = 365*2#+1
    date_list = [start_day - datetime.timedelta(days = x) for x in range(0, numdays)]
    date_list = map(lambda x: x.strftime("%Y%m%d"), date_list)
    playsport_nba_obj = playsport()
    result_2015 = []
    for i in date_list:
        time.sleep(random.randint(1,5))
        print i
        try:
            odds = playsport_nba_obj.basketball_betting_odds('CBA',i)
            result_2015 = result_2015 + odds
            print odds
        except Exception, e:
            f.write(i + '   ' + str(e) + '   ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
            print str(e)
    f.close()
    pickle.dump(result_2015, open('playsport_CBA_2014_2015', "wb" ))

    # nba_obj = NBA_betting_odds()
    # start_day = datetime.datetime.strptime('20151231', "%Y%m%d").date()
    # numdays = 365
    # date_list = [start_day - datetime.timedelta(days = x) for x in range(0, numdays)]
    # date_list = map(lambda x: x.strftime("%Y%m%d"), date_list)
    # result_2015 = []
    # for i in date_list:
    #     print i
    #     try:
    #         odds = nba_obj.get_total_betting_odds(i)
    #         result_2015 = result_2015 + odds
    #         print odds
    #     except Exception, e:
    #         f.write(i + '   ' + str(e) + '   ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    #         print str(e)
    # f.close()
    # pickle.dump(result_2015, open('result_2015', "wb" ))
    #
    #
    # nba_tomorrow_obj = NBA_betting_odds_tomorrow()
    # odds_tomorrow = nba_tomorrow_obj.get_total_betting_odds_tomorrow()
    # for i in odds_tomorrow:
    #     print i
    # print len(odds_tomorrow)
    #
    #
    # f = open('error.log','a')
    # nba_event_obj = NBA_event()
    # start_day = datetime.datetime.strptime('20121231', "%Y%m%d").date()
    # numdays = 366
    # date_list = [start_day - datetime.timedelta(days = x) for x in range(0, numdays)]
    # date_list = map(lambda x: x.strftime("%Y%m%d"), date_list)
    # NBA_event_2012 = []
    # for i in date_list:
    #     print i
    #     try:
    #         odds = nba_event_obj.get_nba_event(i)
    #         NBA_event_2012 = NBA_event_2012 + odds
    #         print odds
    #     except Exception, e:
    #         f.write(i + '   ' + str(e) + '   ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    #         print str(e)
    # f.close()
    # pickle.dump(NBA_event_2012, open('NBA_event_2012', "wb" ))