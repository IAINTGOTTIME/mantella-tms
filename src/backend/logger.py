import logging
import os
import time
from datetime import datetime
from fastapi import Request
from settings import LEVEL

LOG_FILE_NAME = 'logfile/{:%Y-%m-%d}.log'.format(datetime.utcnow())

os.makedirs(os.path.dirname(LOG_FILE_NAME), exist_ok=True)

logger = logging.getLogger()
logger.setLevel(level=LEVEL)
formatter = logging.Formatter(
    fmt="'%(asctime)s | %(levelname)-8s | %(message)s'")
file_handler = logging.FileHandler(
    filename=LOG_FILE_NAME,
    mode='a'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


async def log_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    final_process_time = process_time * 1000
    log_dict = {
        'url': request.url.path,
        'method': request.method,
        'process_time': final_process_time
    }
    logger.info(log_dict)
    return response
