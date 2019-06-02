# /usr/bin/env/python
# coding=utf-8
import re
import sqlite3
import logging
import json
import requests
import datetime
from bs4 import BeautifulSoup
logger = logging.getLogger()

CAIPIAO_URL = 'https://trade.500.com/jczq/'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


def crawl_caipiao():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    html_content = requests.get(CAIPIAO_URL, timeout=5, headers=headers).text
    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.find_all('tr', class_='bet-tb-tr')
    match_list = []

    now = datetime.datetime.now()
    for row in rows:
        # 让时间格式统一成 %Y-%m-%d %H:%M:%S
        trade_start = row['data-matchdate'] + ' ' + row['data-matchtime'] + ':00'
        # 比赛时间一开始，就没有抓数据的价值
        if datetime.datetime.strptime(trade_start, TIME_FORMAT) <= now:
            continue
        # match在彩票网的id
        trade_id = row['data-infomatchid']
        # 编号
        trade_no = row.find('td', class_='td td-no').a.text
        # 赛事
        trade_event = row.find('td', class_='td td-evt').a.text
        team = row.find('td', class_='td td-team').div
        # 主队
        team_l = team.find('span', class_='team-l').text
        # 客队
        team_r = team.find('span', class_='team-r').text

        # 胜平负分数
        scores = row.find('td', class_='td td-betbtn').find('div', class_='betbtn-row itm-rangB1').find_all('p', class_='betbtn')
        if scores:
            score_win = scores[0].span.text
            score_draw = scores[1].span.text
            score_lose = scores[2].span.text
            created_time = now.strftime(TIME_FORMAT)
            match_tuple = (trade_id, trade_no, trade_event, trade_start, team_l,
                           team_r, 0, score_win, score_draw, score_lose, created_time,
                           '{}')
            match_list.append(match_tuple)
        else:
            print(trade_id, trade_no)
    return match_list


def insert_data_to_sqllite():
    data_list = crawl_caipiao()
    conn = sqlite3.connect('caipiao.db')
    conn.executemany('insert into lottery_score '
                     '(trade_id, trade_no, trade_event,'
                     'trade_start, team_l, team_r, concede_point, '
                     'score_win, score_draw, score_lose, extra_field, created_time)'
                     'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     tuple(data_list))
    conn.commit()
    conn.close()


def scraw_caipiao_result():
    RESULT_URL = 'https://trade.500.com/jczq'
    yesterday = datetime.datetime.today().date() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime(DATE_FORMAT)
    params = {'date': yesterday_str}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                      'Safari/537.36'
    }
    html_content = requests.get(CAIPIAO_URL, params=params, timeout=5, headers=headers).text
    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.find_all('tr', class_='bet-tb-tr bet-tb-end')
    now = datetime.datetime.now()
    match_list = []

    for row in rows:
        # match在彩票网的id
        trade_id = row['data-infomatchid']
        #team = row.find('td', class_='td td-team').div
        # 主对客队比分
        team_score = row.find('i', class_='team-vs team-bf').a.text
        # 让球
        concede_point = []
        for point in row.find('td', class_='td td-rang').find_all('p'):
            if point.span:
                #concede_point.append(point.get_text())
                concede_point.append(point.contents[1].strip())
            else:
                concede_point.append(point.text)

        scores = row.find('td', class_='td td-betbtn')
        # .find('div', class_='betbtn-row itm-rangB1').find_all('p', class_='betbtn')

        if scores:
            team_l_result = []
            extra_score = []

            # 不让球的分数
            scores_no_rangqiu = scores.find('div', class_='betbtn-row itm-rangB1')
            team_l_result.append(int(scores_no_rangqiu.find('p', class_='betbtn betbtn-ok')['data-value']))
            score_dict = {}
            score_dict['win_score'] = scores.find_all('p')[0].span.text
            score_dict['draw_score'] = scores.find_all('p')[1].span.text
            score_dict['lose_score'] = scores.find_all('p')[2].span.text
            extra_score.append(score_dict)

            # 让去的分数
            scores_rangqiu = scores.find('div', class_='betbtn-row itm-rangB2')
            team_l_result.append(int(scores_rangqiu.find('p', class_='betbtn betbtn-ok')['data-value']))
            score_dict = {}
            score_dict['win_score'] = scores.find_all('p')[3].span.text
            score_dict['draw_score'] = scores.find_all('p')[4].span.text
            score_dict['lose_score'] = scores.find_all('p')[5].span.text
            extra_score.append(score_dict)
            created_time = now.strftime(TIME_FORMAT)
            match_tuple = (trade_id, team_score, team_l_result[0], concede_point[0], json.dumps(extra_score[0]),
                           created_time)
            match_list.append(match_tuple)
            match_tuple = (trade_id, team_score, team_l_result[1], concede_point[1], json.dumps(extra_score[1]),
                           created_time)
            match_list.append(match_tuple)
        else:
            print(trade_id)

    return match_list


def insert_match_result_to_sqlite():
    data_list = scraw_caipiao_result()
    conn = sqlite3.connect('caipiao.db')
    conn.executemany('insert into lottery_score_result '
                     '(trade_id, team_score, team_l_result, concede_point, extra_score, created_time)'
                     'values (?, ?, ?, ?, ?, ?)', data_list)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    #match_list = crawl_caipiao()
    #insert_data_to_sqllite(match_list)
    #insert_data_to_sqllite()
    #insert_match_result_to_sqlite()
