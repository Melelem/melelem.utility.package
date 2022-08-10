from ._base import ServiceRequestSession


class NERModelService(ServiceRequestSession):
    name = 'soffos-service-model-ner-ontonotes'

    def __init__(self, text: str):
        super().__init__(payload={'text': text})
