import typing as t


T = t.TypeVar('T')


class LazyLoader(t.Generic[T]):
    def __init__(self, load: t.Callable[[], T]):
        self._load = load
        self._value: T = None

    def __call__(self):
        return self.lazy_load()

    def lazy_load(self):
        if self._value is None:
            self._value = self._load()
        return self._value
