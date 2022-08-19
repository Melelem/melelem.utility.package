from ._base import ServiceRequestSession
from typing import List

class CorefService(ServiceRequestSession):
    name = "soffos-service-model-coref"

    def resolve(self, texts: List[str]):

        json = {"texts": texts}

        return self.request(json=json, path="resolve")
        