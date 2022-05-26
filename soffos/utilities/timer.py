from timeit import default_timer
import logging


class Timer:
    def __init__(self, name: str, *name_args):
        self.logger = logging.getLogger(f'timer.{name % name_args}')
        self.start: float = None
        self.end: float = None
        self.elapsed: float = None

    def __enter__(self):
        self.logger.debug('Starting timer.')
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        self.end = default_timer()
        self.elapsed = self.end - self.start
        self.logger.debug('%.4f seconds elapsed.', self.elapsed)
