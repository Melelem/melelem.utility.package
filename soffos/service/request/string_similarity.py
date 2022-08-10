import typing as t

from ._base import ServiceRequestSession


class StringSimilarityService(ServiceRequestSession):
    name = 'soffos-service-string-similarity'

    def __init__(self, a: str, b: t.List[str], threshold: float = None):
        payload = {'a': a, 'b': b}
        if threshold is not None:
            payload['threshold'] = threshold
        super().__init__(payload)
