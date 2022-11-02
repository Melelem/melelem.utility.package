from ._base import ServiceRequestSession
from typing import Union

class AnalyticsService(ServiceRequestSession):
    name = 'soffos-service-analytics'

    def get_question_keywords(
        self,
        client_id: str,
        top_n: int,
        document_ids: list[str] = None,
        filters: dict[str, Union[dict, list, str, int, float, bool]] = None,
        date_from: str = None,
        date_until: str = None
    ):
        """Pull questions stored on ES and generate keywords from them.

        Args:
            client_id (str): Client's id.
            top_n (int): Number of top keywords to return.
            document_ids (list[str], optional): List of document_ids. Limit the keywords to questions asked on these documents. Defaults to None.
            filters (dict[str, Union[dict, list, str, int, float, bool]], optional): Additional filters. Defaults to {}.
            date_from (str, optional): Process questions after this date. Defaults to None.
            date_until (str, optional): Process questions before this date. Defaults to None.
        """
        
        json = {
            "client_id": client_id,
            "top_n": top_n
        }

        if document_ids is not None:
            json["document_ids"] = document_ids
        if filters is not None:
            json["filters"] = filters
        if date_from is not None:
            json["date_from"] = date_from
        if date_until is not None:
            json["date_until"] = date_until

        return self.request(json=json, path="question/keywords")
        