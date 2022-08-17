from unittest import TestCase

from soffos.service.request import (
    BertModelService,
    NERModelService
)


class RequestTests(TestCase):
    def test_bert_model_service(self):
        strs = ['Hello World!']
        response = BertModelService().infer(strs)
        self.assertIn('embeddings', response)

    def test_ner_model_service(self):
        text = 'Bob and Jane got married on the 1st of Jan.'
        response = NERModelService().infer(text)
        self.assertIn('named_entities', response)
