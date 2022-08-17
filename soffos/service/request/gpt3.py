from ._base import ServiceRequestSession


class GPT3Service(ServiceRequestSession):
    name = 'soffos-service-gpt3'

    def generate(
        self,
        prompt: str,
        stop: str,
        max_tokens: int,
        engine: str = None
    ):
        return self.request(
            {
                'prompt': prompt,
                'stop': stop,
                'engine': engine,
                'max_tokens': max_tokens
            },
            path='generate'
        )
