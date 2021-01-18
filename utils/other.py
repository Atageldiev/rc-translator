def get_key_by_value(value: str, dictionary: dict):
    return list(filter(lambda values: values[1] == value, dictionary.items()))[0][0]
