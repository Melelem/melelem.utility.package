import typing as t

from ._base import _Session


# TODO: Split this file into multiple files.


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
