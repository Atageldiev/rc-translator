from loader import translator


def get_translation(text, dest: str = ""):
    return translator.translate(text, dest=dest).text


def get_src(text):
    return translator.translate(text).src
