from unittest import TestCase
from unittest.mock import patch, Mock

from melelem.service import Service, Model, Field, ValidationError


class TextCleaningService(Service):
    class Data(Model):
        text: str = Field()

    def run(self, data: Data):
        return data.text.strip()


class AgeIncrementorService(Service):
    class Data(Model):
        age: int = Field()

    def run(self, data: Data):
        return data.age + 1


class ServiceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = TextCleaningService()

    @patch.object(TextCleaningService, 'initialize')
    def test_singelton(self, initialize: Mock):
        service = TextCleaningService()
        self.assertEqual(service, self.service)
        initialize.assert_not_called()

    def test_singleton__multiple_services(self):
        with patch.object(AgeIncrementorService, 'initialize') as initialize:
            age_incrementor_service = AgeIncrementorService()
            age_incrementor_service_2 = AgeIncrementorService()
            self.assertEqual(age_incrementor_service, age_incrementor_service_2)
            initialize.assert_called_once()

        with patch.object(TextCleaningService, 'initialize') as initialize:
            text_cleaning_service = TextCleaningService()
            self.assertEqual(text_cleaning_service, self.service)
            initialize.assert_not_called()

    def test_validate(self):
        text = 'abc'
        data = self.service.validate(text=text)
        self.assertEqual(data.text, text)

    def test_validate__unknown_field(self):
        with self.assertRaises(ValidationError):
            self.service.validate(number=1)

    def test_serve(self):
        text = ' hi '
        clean_text = self.service.serve(text=text)
        self.assertEqual(clean_text, text.strip())
