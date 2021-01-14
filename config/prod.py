import logging
import os
from .common import *

TOKEN = "1368801526:AAFoG3C84uthcDinURZ031e2WOt9fcUzTjM"

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DB = os.getenv("DB_DB")

logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(BASE_DIR, ".log"),
                    format='ID-%(process)d:%(asctime)s:%(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
