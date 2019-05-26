# /usr/bin/env/python
# coding=utf-8

from bs4 import BeautifulSoup
import requests
import datetime
import sqlite3

CAIPIAO_URL = 'https://trade.500.com/jczq/'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def crawl_caipiao():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    html_content = requests.get(CAIPIAO_URL, timeout=5, headers=headers).text
    soup = BeautifulSoup(html_content)
    rows = soup.find_all('tr', class_='bet-tb-tr')
    match_list = []

    now = datetime.datetime.now()
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    for row in rows:
        trade_start = row['data-matchdate'] + ' ' + row['data-matchtime'] + ':00'
        #trade_start = row.find('td', class_='td td-endtime').text
        # trade_start format 05-27 06:00
        # 让时间格式统一成 %Y-%m-%d %H:%M:%S
        #trade_start_str = str(now.year) + '-' + ':00'
        # 比赛时间一开始，就没有抓数据的价值
        if datetime.datetime.strptime(trade_start, TIME_FORMAT) <= now:
            continue
        # match在彩票网的id
        trade_id = row['data-infomatchid']
        # 编号
        trade_no = row.find('td', class_='td td-no').a.text
        # 赛事
        trade_event = row.find('td', class_='td td-evt').a.text
        # 开赛时间
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


if __name__ == '__main__':
    #insert_data_to_sqllite(crawl_caipiao())
    match_list = crawl_caipiao()
    insert_data_to_sqllite(match_list)
