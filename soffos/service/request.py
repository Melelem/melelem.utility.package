import typing as t

from ..settings import get_service_url, DEBUG
from ..web import RetryWebClient


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
            url = get_service_url(self.name)
        super().__init__(payload, url)

    def send(self):
        return super().send()['response']


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
