from re import S
from ._base import ServiceRequestSession
from typing import List, Dict, Any

class QuestionAnsweringService(ServiceRequestSession):
    name = "soffos-service-question-answering"

    def answer(
        self,
        message: str,
        meta: dict = None,
        llm_api_key: str = None,
        user:str = None,
        client_id: str = None,
        document_ids: List[str] = None,
        document_dicts: List[Dict[str, Any]] = None,
        document_text: str = None,
        message_id: str = None,
        session_id: str = None,
        store_question: bool = None,
        invoke_previous_questions: bool = None,
        check_ambiguity: bool = None,
        check_query_type: bool = None,
        generic_response: bool = None
    ):

        json = {"message": message}
        if meta is not None:
            json['meta'] = meta
        if llm_api_key is not None:
            json['llm_api_key'] = llm_api_key,
        if user is not None:
            json['user'] = user
        if client_id is not None:
            json["client_id"] = client_id
        if document_ids is not None:
            json["document_ids"] = document_ids
        if document_dicts is not None:
            json["document_dicts"] = document_dicts
        if document_text is not None:
            json["document_text"] = document_text
        if message_id is not None:
            json["message_id"] = message_id
        if session_id is not None:
            json["session_id"] = session_id
        if store_question is not None:
            json["store_question"] = store_question
        if invoke_previous_questions is not None:
            json["invoke_previous_questions"] = invoke_previous_questions
        if check_ambiguity is not None:
            json["check_ambiguity"] = check_ambiguity
        if check_query_type is not None:
            json["check_query_type"] = check_query_type
        if generic_response is not None:
            json["generic_response"] = generic_response

        return self.request(json=json, path="answer")
