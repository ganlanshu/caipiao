# coding=utf-8

import logging
import os
import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(ROOT_DIR, 'logs')
LOG_FILE = 'scrawl_stderr_{}.log'.format(datetime.date.today().strftime('%Y%m%d'))

logger = logging.getLogger('main')
handler = logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE))
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(lineno)d %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('ilove you')
