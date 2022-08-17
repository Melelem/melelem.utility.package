import typing as t

from ._base import ServiceRequestSession


class ProfanityModelService(ServiceRequestSession):
    name = 'soffos-service-profanity'

    def infer(self, strings: t.List[str]):
        return self.request({'strings': strings})
