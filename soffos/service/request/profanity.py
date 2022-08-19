from ._base import ServiceRequestSession
from typing import List

class ProfanityService(ServiceRequestSession):
    name = 'soffos-service-profanity'

    def detect(self, strings: List[str]):
        return self.request(json={"strings": strings})
