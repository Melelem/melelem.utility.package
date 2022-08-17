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
        max_tokens: int = None,
        engine: str = None,
        chunk_max_sentences: int = None,
        chunk_sentence_overlap: int = None
    ):
        json = {'text': text}
        if max_tokens is not None:
            json['max_tokens'] = max_tokens
        if engine is not None:
            json['engine'] = engine
        if chunk_max_sentences is not None:
            json['chunk_max_sentences'] = chunk_max_sentences
        if chunk_sentence_overlap is not None:
            json['chunk_sentence_overlap'] = chunk_sentence_overlap
        return self.request(json, response_cls=self.GenerateQnAListResponse)
