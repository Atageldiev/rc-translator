import logging
import os

from core.conf.settings import BASE_DIR, DEBUG

logger = logging.getLogger("main")

formatter = logging.Formatter(fmt='ID-%(process)d:%(asctime)s:%(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                              datefmt='%d-%b-%y %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename=os.path.join(BASE_DIR, ".log"))
file_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
if not DEBUG:
    logger.addHandler(file_handler)
