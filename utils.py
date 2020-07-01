from aiogram.utils.helper import Helper, HelperMode, ListItem


class States(Helper):
    mode = HelperMode.snake_case

    STATE_CHOOSE_LANG_INTO = ListItem()
    STATE_SEND_WORD = ListItem()
    STATE_SEND_RESULT = ListItem()
    # STATE_0 = ListItem()
    # STATE_0 = ListItem()
