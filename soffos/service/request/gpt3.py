from ._base import ServiceRequestSession


class GPT3Service(ServiceRequestSession):
    name = 'soffos-service-gpt3'
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
