import typing as t

from ...settings import get_service_url
from ...web import RetryWebClient


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
