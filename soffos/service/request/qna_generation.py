import typing as t

from pydantic import BaseModel

from ...pre_processing import Chunk
from ._base import ServiceRequestSession


# TODO: Abstract this class into base class.
class QnAGenerationService(ServiceRequestSession):
    name = 'soffos-service-qna-generation'

    class GenerateQnAListResponse(BaseModel):
        qna_list: t.List[t.Dict[str, t.Any]]
        usage_overview: t.Dict[str, t.Any]
        chunks: t.List[Chunk]

    def generate_qna_list(
        self,
        text: str,
        llm_api_key: str = None,
        max_tokens: int = None,
        engine: str = None,
        chunk_max_sentences: int = None,
        chunk_sentence_overlap: int = None,
        user: str = None
    ):
        json = {'text': text}
        if llm_api_key is not None:
            json['llm_api_key'] = llm_api_key
        if max_tokens is not None:
            json['max_tokens'] = max_tokens
        if engine is not None:
            json['engine'] = engine
        if chunk_max_sentences is not None:
            json['chunk_max_sentences'] = chunk_max_sentences
        if chunk_sentence_overlap is not None:
            json['chunk_sentence_overlap'] = chunk_sentence_overlap
        if user is not None:
            json['user'] = user
        return self.request(json, response_type=self.GenerateQnAListResponse)
