#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging

from aiogram.types import CallbackQuery

from loader import dp, parser


#---------------------------------------------------------------------------
#   Functions
#---------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == "show_examples")
async def show_examples(callback_query: CallbackQuery):
    """
    Sends 4 more examples, if available
    If not, converts text of the message that button is pinned to into "All of the examples have already been shown"
    """
    user_id = callback_query.from_user.id
    data = await dp.storage.get_data(user=user_id)

    num = data["num"]

    await callback_query.answer("Loading...")
    await parser.parse_examples(data, callback_query.message, num)
    
    await dp.storage.update_data(user=callback_query.from_user.id, data={"num": num + 3})
    

