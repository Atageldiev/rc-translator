from googletrans import Translator

translator = Translator()


def get_translation(text, dest: str = ""):
    return translator.translate(text, dest=dest).text


def get_src(text):
    return translator.translate(text).src
