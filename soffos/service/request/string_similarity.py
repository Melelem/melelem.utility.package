import typing as t

from ._base import ServiceRequestSession


class StringSimilarityService(ServiceRequestSession):
    name = 'soffos-service-string-similarity'

    def get_similarities(
        self,
        a: str,
        b: t.List[str],
        threshold: float = None
    ):
        json = {'a': a, 'b': b}
        if threshold is not None:
            json['threshold'] = threshold
        return self.request(json)
