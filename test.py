# /usr/bin/env/python
# coding=utf-8

from bs4 import BeautifulSoup
import requests
import datetime

CAIPIAO_URL = 'https://trade.500.com/jczq/'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def crawl_caipiao():
    html_content = requests.get(CAIPIAO_URL, timeout=5).text
    soup = BeautifulSoup(html_content)
    rows = soup.find_all('tr', class_='bet-tb-tr')
    match_list = []

    #now = datetime.datetime.now().strftime()
    for row in rows:
        match_dict = {}
        trade_no = row.find('td', class_='td td-no').a.text
        # 编号
        match_dict['trade_no'] = trade_no
        # 赛事
        match_dict['trade_event'] = row.find('td', class_='td td-evt').a.text
        # 开赛时间
        match_dict['trade_end'] = row.find('td', class_='td td-endtime').text
        # team
        team = row.find('td', class_='td td-team').div
        # 主队
        team_l = team.find('span', class_='team-l').text
        # 客队
        team_r = team.find('span', class_='team-r').text
        match_dict['team_l'] = team_l
        match_dict['team_r'] = team_r
        match_list.append(match_dict)
    return match_list









headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

url = 'https://book.douban.com/top250'

def get_info2(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html)

    for link in soup.find_all('tr', attrs={"class": "item"}):

        #name = link.find("a")
        info = link.find('p')
        #print(info.text)

        title = link.find('div')
        print((str(title.a.text)).strip())

        #quote = link.find('span',class_="inq")

        #if quote:
        #    print quote.text


if __name__ == '__main__':
    match_list = crawl_caipiao()
    print(match_list)


