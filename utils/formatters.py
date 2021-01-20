BOLD = "<b>{}</b>"
UNDERLINED = "<u>{}</u>"
CURSIVE = "<em>{}</em>"


def bold(text):
    return BOLD.format(text)


def underlined(text):
    return UNDERLINED.format(text)


def bold_underlined(text):
    return bold(underlined(text))


def cursive(text):
    return CURSIVE.format(text)
