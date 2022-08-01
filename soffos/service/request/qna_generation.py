import typing as t

from pydantic import BaseModel

from ...pre_processing import Chunk
from ._base import _Session


# TODO: Abstract this class into base class.
class QnAGenerationService(_Session):
    name = 'SOFFOS_SERVICE_QNA_GENERATION'

    def __init__(
        self,
        text: str,
        max_tokens: int = None,
        engine: str = None,
        chunk_max_sentences: int = None,
        chunk_sentence_overlap: int = None
    ):
        payload = {'text': text}
        if max_tokens is not None:
            payload['max_tokens'] = max_tokens
        if engine is not None:
            payload['engine'] = engine
        if chunk_max_sentences is not None:
            payload['chunk_max_sentences'] = chunk_max_sentences
        if chunk_sentence_overlap is not None:
            payload['chunk_sentence_overlap'] = chunk_sentence_overlap
        super().__init__(payload)

    class Response(BaseModel):
        qna_list: t.List[t.Dict[str, t.Any]]
        usage_overview: t.Dict[str, t.Any]
        chunks: t.List[Chunk]

    def send(self):
        response = super().send()
        return self.Response(**response)
