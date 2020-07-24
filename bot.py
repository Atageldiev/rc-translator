import handlers                                                         # import handlers for: callbacks, commands, admin commands, states

from aiogram import executor
from loader import dp



if __name__ == '__main__':
 
    from modules import setTask    
    
    dp.loop.create_task(setTask())                     
    executor.start_polling(
        dp, 
        skip_updates=True
        )
        # on_startup=BackUp()
        # on_shutdown=BackUp())                       
    