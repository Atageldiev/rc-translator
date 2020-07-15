from aiogram.utils.helper import Helper, HelperMode, ListItem


class WordStates(Helper):
    mode = HelperMode.snake_case

    STATE_CHOOSE_LANG_INTO = ListItem()
    STATE_SEND_WORD = ListItem()
    STATE_SEND_RESULT = ListItem()

class AdminStates(Helper):
    mode = HelperMode.snake_case

    STATE_SEND_MESSAGE_ALL = ListItem()
    STATE_SETDB = ListItem()

class LearnerStates(Helper):
    mode = HelperMode.snake_case
    
    STATE_CHOOSE_MODE = ListItem()
