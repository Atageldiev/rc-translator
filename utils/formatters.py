BOLD = "<b>{}</b>"
UNDERLINED = "<u>{}</u>"
CURSIVE = "<em>{}</em>"


def bold(text):
    """Returns bold text"""
    return BOLD.format(text)


def underlined(text):
    """Returns underlined text"""
    return UNDERLINED.format(text)


def bold_underlined(text):
    """Returns text that is bold and underlined at the same time"""
    return bold(underlined(text))


def cursive(text):
    """Returns cursive text"""
    return CURSIVE.format(text)


def strip_text(text: str) -> str:
    """Returns a text without any extra spaces anywhere"""
    return " ".join(text.split())
