BOLD = "<b>{}</b>"
UNDERLINED = "<u>{}</u>"
CURSIVE = "<em>{}</em>"


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
