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
def get_translation(text, data: dict = {}, dest: str = ""):
    if not dest:
        dest = LANGCODES.get(data["dest"])
        
    return translator.translate(text, dest=dest).text


async def setTask():
    scheduler()
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()
    
