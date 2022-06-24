import typing as t

from ..settings import get_service_url
from ..web import RetryWebClient


class NERModelService(RetryWebClient):
    def __init__(self, text: str):
        super().__init__(
            payload={'text': text},
            url=get_service_url('SOFFOS_SERVICE_MODEL_NER_ONTONOTES')
        )


class ProfanityModelService(RetryWebClient):
    """
    Profanity model service. Activates remote service with neural network
    processing capabilities.
    """

    def __init__(self, strings: t.List[str]):
        super().__init__(
            payload={'strings': strings},
            url=get_service_url('SOFFOS_SERVICE_MODEL_PROFANITY')
        )


class BertModelService(RetryWebClient):
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

        super().__init__(
            payload=payload,
            url=get_service_url('SOFFOS_SERVICE_MODEL_BERT')
        )
