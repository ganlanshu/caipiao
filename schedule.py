# coding=utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from spider import insert_data_to_sqllite, insert_match_result_to_sqlite


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(insert_data_to_sqllite, 'interval', minutes=5)
    scheduler.start()
