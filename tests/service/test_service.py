from unittest import TestCase

from soffos.service import Service, DataModel, DataField, DataValidationError


class TextCleaningService(Service):
    class Data(DataModel):
        text: str = DataField()

    def run(self, data: Data):
        return data.text.strip()


class ServiceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = TextCleaningService()

    def test_validate(self):
        text = 'abc'
        data = self.service.validate(text=text)
        self.assertEqual(data.text, text)

    def test_validate__unknown_field(self):
        with self.assertRaises(DataValidationError):
            self.service.validate(number=1)

    def test_serve(self):
        text = ' hi '
        clean_text = self.service.serve(text=text)
        self.assertEqual(clean_text, text.strip())
