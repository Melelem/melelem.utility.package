import typing as t
import logging
import sys


def configure_logger(
    logger: t.Union[logging.Logger, str] = None,
    level: str = 'INFO',
    fmt: str = '[%(asctime)s][%(process)d][%(thread)d][%(name)s][%(levelname)s] - %(message)s',
    fmt_style: str = '%',
    stream: t.TextIO = sys.stderr
):
    logger = (
        logger
        if isinstance(logger, logging.Logger)
        else logging.getLogger(logger)
    )
    logger.setLevel(level)

    formatter = logging.Formatter(fmt, style=fmt_style)

    def configure_handler(handler: logging.Handler):
        handler.setLevel(level)
        handler.setFormatter(formatter)

    if logger.handlers:
        for handler in logger.handlers:
            configure_handler(handler)
    else:
        stream_handler = logging.StreamHandler(stream)
        configure_handler(stream_handler)
        logger.addHandler(stream_handler)

    return logger
