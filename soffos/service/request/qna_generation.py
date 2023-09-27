import typing as t

from ...pre_processing import Chunk
from ._base import ServiceRequestSession


# TODO: Abstract this class into base class.
class QnAGenerationService(ServiceRequestSession):
    name = 'soffos-service-qna-generation'

    def generate_qna_list(
        self,
        text: str,
        llm_api_key: str = None,
        max_tokens: int = None,
        engine: str = None,
        sentence_split: int = None,
        sentence_overlap: int = None,
        user: str = None
    ):
        json = {'text': text}
        if llm_api_key is not None:
            json['llm_api_key'] = llm_api_key
        if max_tokens is not None:
            json['max_tokens'] = max_tokens
        if engine is not None:
            json['engine'] = engine
        if sentence_split is not None:
            json['sentence_split'] = sentence_split
        if sentence_overlap is not None:
            json['sentence_overlap'] = sentence_overlap
        if user is not None:
            json['user'] = user
            
        return self.request(json)
