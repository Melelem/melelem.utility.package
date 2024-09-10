from ._base import ServiceRequestSession
from typing import List


class StanzaService(ServiceRequestSession):
    name = "melelem-service-model-stanza"

    def annotate(self, texts: List[str]):

        json = {"texts": texts}

        return self.request(json=json, path="annotate", response_type=bytes)
