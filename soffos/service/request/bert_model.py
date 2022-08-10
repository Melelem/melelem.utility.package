import typing as t

from ._base import ServiceRequestSession


class BertModelService(ServiceRequestSession):
    name = 'soffos-service-model-bert'

    def __init__(
        self,
        strs: t.List[str],
        max_length: int = None,
        truncation: bool = None,
        padding: str = None
    ):
        payload = {'strs': strs}
        if max_length is not None:
            payload['max_length'] = max_length
        if truncation is not None:
            payload['truncation'] = truncation
        if padding is not None:
            payload['padding'] = padding
        super().__init__(payload)
