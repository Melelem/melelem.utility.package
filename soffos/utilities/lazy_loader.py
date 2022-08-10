import typing as t


T = t.TypeVar('T')


class LazyLoader(t.Generic[T]):
    def __init__(self, load: t.Callable[[], T]):
        self._load = load
        self._value: T = None
        self._did_load = False

    def __call__(self):
        return self.lazy_load()

    def lazy_load(self):
        if not self._did_load:
            self._value = self._load()
            self._did_load = True
        return self._value
