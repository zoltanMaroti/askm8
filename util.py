from datetime import datetime


def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def make_string(dictonary):
    values = ""
    for value in dictonary.values():
        values += f", {values}"
    return values
