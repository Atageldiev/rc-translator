from google_trans_new import google_translator

translator = google_translator()


def translate(text, dest: str = ""):
    translation = translator.translate(text, lang_tgt=dest)
    return " && ".join(translation) if isinstance(translation, list) else translation


def detect(text):
    return translator.detect(text)[0]
