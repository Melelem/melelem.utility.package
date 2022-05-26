import typing as t
import logging
import sys


def configure_root_logger(
    level: str = 'INFO',
    fmt: str = '[%(asctime)s][%(process)d][%(thread)d][%(name)s][%(levelname)s] - %(message)s',
    fmt_style: str = '%',
    stream: t.TextIO = sys.stdout
):
    formatter = logging.Formatter(fmt, style=fmt_style)

    stream_handler = logging.StreamHandler(stream)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(stream_handler)

    return logger
