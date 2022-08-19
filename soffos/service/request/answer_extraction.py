from ._base import ServiceRequestSession
from typing import List

class AnswerExtractionService(ServiceRequestSession):
    name = 'soffos-service-model-answer-extraction'

    def answer(
        self,
        question: str,
        documents: List[dict],
        top_k: int = None
    ):

        json = {
            "question": question,
            "documents": documents
        }
        if top_k:
            json["top_k"] = top_k

        return self.request(json=json, path="answer")