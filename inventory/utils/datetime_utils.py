from datetime import datetime


def date_from_string(text: str):
    return datetime.strptime(text, '%B %d, %Y').date()
