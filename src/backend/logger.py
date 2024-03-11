import logging
import time
from datetime import datetime
from fastapi import Request
from settings import LEVEL
# root = os.path.dirname("__file__")
# with open(os.path.join(root, "ENV/logger_lvl"), 'r') as file:
#     LEVEL = file.read()
# level = logging.getLevelName(LoggerSettings.logger_lvl)
logger = logging.getLogger()
logger.setLevel(level=LEVEL)
formatter = logging.Formatter(fmt="'%(asctime)s | %(levelname)-8s | %(message)s'")
file_handler = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.utcnow()))
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
