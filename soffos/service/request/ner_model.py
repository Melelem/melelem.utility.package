from ._base import ServiceRequestSession


class NERModelService(ServiceRequestSession):
    name = 'soffos-service-model-ner-ontonotes'

    def infer(self, text: str):
        return self.request({'text': text})
