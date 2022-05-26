from timeit import default_timer
import logging


class Timer:
    def __init__(self, name: str, *name_args, log_level: int = logging.DEBUG):
        self.logger = logging.getLogger(f'timer.{name % name_args}')
        self.log_level = log_level
        self.start: float = None
        self.end: float = None
        self.elapsed: float = None

    def __enter__(self):
        self.logger.log(self.log_level, 'Starting timer.')
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        self.end = default_timer()
        self.elapsed = self.end - self.start
        self.logger.log(self.log_level, '%.4f seconds elapsed.', self.elapsed)
