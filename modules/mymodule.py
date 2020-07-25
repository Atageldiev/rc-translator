#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging 
import asyncio
import schedule

from loader import translator
from data.config import LANGCODES
from .learner import scheduler

#---------------------------------------------------------------------------
#   Functions
#---------------------------------------------------------------------------
def get_translation(text, dest: str = ""):      
    return translator.translate(text, dest=dest).text

def get_src(text):
    return translator.translate(text).src

async def setTask():
    scheduler()
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()
    
