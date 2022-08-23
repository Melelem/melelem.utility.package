from re import S
from ._base import ServiceRequestSession
from typing import List, Dict, Any

class QuestionAnsweringService(ServiceRequestSession):
    name = "soffos-service-question-answering"

    def answer(
        self,
        message: str,
        client_id: str = None,
        document_ids: List[str] = None,
        document_dicts: List[Dict[str, Any]] = None,
        document_text: str = None,
        message_id: str = None,
        session_id: str = None,
        qa_type: str = None,
        store_question: bool = None
    ):

        json = {"message": message}
        if client_id is not None:
            json["client_id"] = client_id
        if document_ids is not None:
            json["document_ids"] = document_ids
        if document_dicts is not None:
            json["document_dicts"] = document_dicts
        if document_text is not None:
            json["document_text"] = document_text
        if message_id is not None:
            json["qa_type"] = qa_type
        if session_id is not None:
            json["session_id"] = session_id
        if store_question is not None:
            json["store_question"]

        return self.request(json=json, path="answer")
