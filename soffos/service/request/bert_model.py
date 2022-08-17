import typing as t

from ._base import ServiceRequestSession


class BertModelService(ServiceRequestSession):
    name = 'soffos-service-model-bert'

    def infer(
        self,
        strs: t.List[str],
        max_length: int = None,
        truncation: bool = None,
        padding: str = None
    ):
        json = {'strs': strs}
        if max_length is not None:
            json['max_length'] = max_length
        if truncation is not None:
            json['truncation'] = truncation
        if padding is not None:
            json['padding'] = padding
        return self.request(json)
