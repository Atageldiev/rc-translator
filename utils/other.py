def get_key_by_value(value: str, dictionary: dict):
    try:
        return list(filter(lambda values: values[1] == value, dictionary.items()))[0][0]
    except:
        return None
