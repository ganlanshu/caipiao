# coding=utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from log_config import logger
from spider import insert_data_to_sqllite, insert_match_result_to_sqlite

log = logging.getLogger('scrawl.match')

if __name__ == '__main__':
    #scheduler = BackgroundScheduler()
    scheduler = BlockingScheduler()
    try:
        scheduler.add_job(insert_data_to_sqllite, 'interval', minutes=5)
        scheduler.add_job(insert_match_result_to_sqlite, 'cron', hour=6, minute=0)
        scheduler.start()
    except Exception as e:
        print(e)
        log.error(str(e))
