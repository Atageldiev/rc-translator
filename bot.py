import handlers                                                         # import callback, command, admin command, states handlers

from aiogram import executor
from loader import dp

if __name__ == '__main__':
    from modules.mymodule import setTask                                # import task that preforms scheduled stuff 

    dp.loop.create_task(setTask())                                      # Create a new task in dp.loop
    executor.start_polling(dp, skip_updates=True)                       # Start bot polling
    
