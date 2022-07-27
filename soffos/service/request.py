import typing as t
from dataclasses import asdict

from ..settings import get_service_url, DEBUG
from ..web import RetryWebClient
from ..pre_processing import Chunk


class _Session(RetryWebClient):
    name: str
    path = ''

    def __init__(self, payload):
        if DEBUG:
            payload = {
                'name': self.name,
                'request': payload
            }
            if self.path:
                payload['path'] = self.path
            url = 'https://dev-api.soffos.ai/api/service/'
        else:
            url = get_service_url(self.name) + self.path
        super().__init__(payload, url)

    def send(self):
        response = super().send()
        if DEBUG:
            response = response['response']
        return response


class GPT3Service(_Session):
    name = 'SOFFOS_SERVICE_GPT3'
    path = 'generate'

    def __init__(self, prompt: str, stop: str, max_tokens: int, engine: str = None):
        super().__init__(
            payload={
                'prompt': prompt,
                'stop': stop,
                'engine': engine,
                'max_tokens': max_tokens
            }
        )


class NERModelService(_Session):
    name = 'SOFFOS_SERVICE_MODEL_NER_ONTONOTES'

    def __init__(self, text: str):
        super().__init__(payload={'text': text})


class ProfanityModelService(_Session):
    name = 'SOFFOS_SERVICE_MODEL_PROFANITY'

    def __init__(self, strings: t.List[str]):
        super().__init__(payload={'strings': strings})


class QATransformersModelService(_Session):
    name = 'SOFFOS_SERVICE_MODEL_QA_TRANSFORMERS'

    def __init__(self, context: str, question: str):
        super().__init__(payload={'context': context, 'question': question})


class BertModelService(_Session):
    name = 'SOFFOS_SERVICE_MODEL_BERT'

    def __init__(
        self,
        strs: t.List[str],
        max_length: int = None,
        truncation: bool = None,
        padding: str = None
    ):
        payload = {'strs': strs}
        if max_length is not None:
            payload['max_length'] = max_length
        if truncation is not None:
            payload['truncation'] = truncation
        if padding is not None:
            payload['padding'] = padding
        super().__init__(payload)


class QnAGenerationService(_Session):
    name = 'SOFFOS_SERVICE_QNA_GENERATION'

    def __init__(
        self,
        text: str = None,
        chunks: t.List[Chunk] = None,
        max_tokens: int = None,
        engine: str = None,
        chunk_max_sentences: int = None,
        chunk_sentence_overlap: int = None
    ):
        payload = {}
        if text is not None:
            payload['text'] = text
        if chunks is not None:
            payload['chunks'] = [asdict(chunk) for chunk in chunks]
        if max_tokens is not None:
            payload['max_tokens'] = max_tokens
        if engine is not None:
            payload['engine'] = engine
        if chunk_max_sentences is not None:
            payload['chunk_max_sentences'] = chunk_max_sentences
        if chunk_sentence_overlap is not None:
            payload['chunk_sentence_overlap'] = chunk_sentence_overlap
        super().__init__(payload)


class StringSimilarityService(_Session):
    name = 'SOFFOS_SERVICE_STRING_SIMILARITY'

    def __init__(self, a: str, b: t.List[str], threshold: float = None):
        payload = {'a': a, 'b': b}
        if threshold is not None:
            payload['threshold'] = threshold
        super().__init__(payload)


class TagService(_Session):
    name = 'SOFFOS_SERVICE_TAG'

    def __init__(
        self,
        texts: t.List[str],
        language: str = None,
        options_one_word: bool = None,
        options_two_words: bool = None,
        options_three_words: bool = None,
    ):
        payload = {'texts': texts, 'options': {}}
        if language is not None:
            payload['language'] = language
        if options_one_word is not None:
            payload['options']['one_word'] = options_one_word
        if options_two_words is not None:
            payload['options']['two_words'] = options_two_words
        if options_three_words is not None:
            payload['options']['three_words'] = options_three_words
        super().__init__(payload)
