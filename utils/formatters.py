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


class FormattedText:
    def __init__(self, text):
        self.text = text

    def bold(self):
        """Returns bold text"""
        return self.__class__(BOLD.format(self.text))

    def strip(self):
        """Returns a text without any extra spaces anywhere"""
        return self.__class__(" ".join(self.text.split()))

    def cursive(self):
        """Returns cursive text"""
        return self.__class__(CURSIVE.format(self.text))

    def underlined(self):
        """Returns underlined text"""
        return self.__class__(UNDERLINED.format(self.text))

    def __str__(self):
        return self.text
