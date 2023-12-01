import logging
from datetime import datetime
from functools import lru_cache

from colorful_print import color


def get_today_date_format(date_format: str = "%Y-%m-%d %H:%M:%S"):
    return datetime.today().strftime(date_format)


@lru_cache
def get_logger():
    formatter = logging.Formatter(
        "[%(levelname)s]\t %(asctime)s\t %(pathname)s:%(lineno)d\t\t %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S",
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("stock-visualize")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger


def colorful_dispatcher(c: str, *args, **kwargs):
    dispatch = getattr(color, c)
    dispatch(*args, **kwargs)


def red(*args, **kwargs):
    colorful_dispatcher("red", *args, **kwargs)


def yellow(*args, **kwargs):
    colorful_dispatcher("yellow", *args, **kwargs)


def green(*args, **kwargs):
    colorful_dispatcher("green", *args, **kwargs)


def blue(*args, **kwargs):
    colorful_dispatcher("blue", *args, **kwargs)


def magenta(*args, **kwargs):
    colorful_dispatcher("magenta", *args, **kwargs)


def white(*args, **kwargs):
    colorful_dispatcher("white", *args, **kwargs)
