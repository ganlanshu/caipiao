# coding=utf-8

import logging
import os
import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(ROOT_DIR, 'logs')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_handler = logging.FileHandler(os.path.join(LOG_DIR, 'scrawl_stdout.log'))
stderr_handler = logging.FileHandler(os.path.join(LOG_DIR, 'scrawl_stderr.log'))
formatter = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(lineno)d %(message)s'
)
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)
