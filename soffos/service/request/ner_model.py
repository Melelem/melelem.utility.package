from ._base import ServiceRequestSession


class NERModelService(ServiceRequestSession):
    name = 'soffos-service-model-ner-ontonotes'

    def infer(self, text: str = None, texts: list[str] = None):

        json = {}

        if text is not None:
            json['text'] = text
        if texts is not None:
            json['texts'] = texts

        return self.request(json=json)
