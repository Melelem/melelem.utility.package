from ._base import ServiceRequestSession
from typing import List

class CorefModelService(ServiceRequestSession):
    name = "metal-service-model-coref"

    def resolve(self, texts: List[str], pronouns: List[str] = None):

        json = {"texts": texts}

        if pronouns is not None:
            json["pronouns"] = pronouns

        return self.request(json=json, path="resolve")
        