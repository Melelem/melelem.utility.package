from ._base import ServiceRequestSession
from typing import List

class SummarizationService(ServiceRequestSession):
    name = "soffos-service-summarization"

    def summarize_abstractive(
        self,
        text: str,
        sent_length: int,
        simplify: bool = None,
        engine: str = None
    ):

        json = {
            "text": text,
            "sent_length": sent_length
        }
        if simplify is not None:
            json["simplify"] = simplify
        if engine is not None:
            json["engine"] = engine
        
        return self.request(json=json, path="abstractive")

    def summarize_extractive(
        self,
        text: str,
        sent_length: int
    ):

        json = {
            "text": text,
            "sent_length": sent_length
        }
        
        return self.request(json=json, path="extractive")
