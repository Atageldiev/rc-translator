import logging
import os

from dotenv import load_dotenv

from .common import *

load_dotenv()

TOKEN = "1397404758:AAEBfHXgaxWM0j-FGnsFsUxQjo4sMuyEz5Q"
print(BASE_DIR)

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DB = os.getenv("DB_DB")

logging.basicConfig(level=logging.INFO,
                    format='ID-%(process)d:%(asctime)s:%(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
