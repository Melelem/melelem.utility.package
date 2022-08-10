from ._base import ServiceRequestSession


class QATransformersModelService(ServiceRequestSession):
    name = 'soffos-service-model-qa-transformers'

    def __init__(self, context: str, question: str):
        super().__init__(payload={'context': context, 'question': question})
