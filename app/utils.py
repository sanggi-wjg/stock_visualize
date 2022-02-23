from datetime import datetime


def get_today_date_format(date_format: str = '%Y-%m-%d %H:%M:%S'):
    return datetime.today().strftime(date_format)
