# coding=utf-8

import datetime
from spider import insert_match_result_to_sqlite
import logging
from log_config import logger

log = logging.getLogger('scrawl.result')
DATE_FORMAT = '%Y-%m-%d'


def scrawl_and_insert_last_month_result():
    day = datetime.datetime.now()
    month_day = 30
    while month_day > 0:
        try:
            insert_match_result_to_sqlite(day)
        except Exception as e:
            log.error(str(e))
            log.error('match on day %s can not scrawl score result' % day.strftime(DATE_FORMAT))

        day -= datetime.timedelta(days=1)
        month_day -= 1


if __name__ == '__main__':
    scrawl_and_insert_last_month_result()
