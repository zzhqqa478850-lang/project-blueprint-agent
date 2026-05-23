# utils/validators.py

import re


def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def validate_username(username):
    if len(username) < 3 or len(username) > 30:
        return False
    return True
