import typing as t

from ._base import ServiceRequestSession


class ProfanityModelService(ServiceRequestSession):
    name = 'soffos-service-profanity'

    def __init__(self, strings: t.List[str]):
        super().__init__(payload={'strings': strings})
