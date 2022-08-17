from ._base import ServiceRequestSession


class QATransformersModelService(ServiceRequestSession):
    name = 'soffos-service-model-qa-transformers'

    def infer(self, context: str, question: str):
        return self.request({'context': context, 'question': question})
