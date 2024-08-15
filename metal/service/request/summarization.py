from ._base import ServiceRequestSession
from typing import List

class SummarizationService(ServiceRequestSession):
    name = "metal-service-summarization"

    def summarize(
        self,
        text: str,
        sent_length: int,
        llm_api_key: str = None,
        user: str = None,
        engine: str = None
    ):

        json = {
            "text": text,
            "sent_length": sent_length
        }
        if llm_api_key is not None:
            json['llm_api_key'] = llm_api_key
        if user is not None:
            json['user'] = user
        if engine is not None:
            json["engine"] = engine
        
        return self.request(json=json)
