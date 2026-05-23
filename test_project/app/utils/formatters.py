# utils/formatters.py

from datetime import datetime


def format_date(date):
    if isinstance(date, datetime):
        return date.strftime('%Y-%m-%d')
    return str(date)


def format_email(email):
    if not email:
        return ''
    return email.lower().strip()
