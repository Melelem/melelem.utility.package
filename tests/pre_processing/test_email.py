from unittest import TestCase

from metal.pre_processing.email import Email


class EmailTests(TestCase):
    def test_from_text(self):
        text = 'His email is john.doe@metal.ai.'
        emails = Email.from_text(text)
        self.assertListEqual(emails, [
            Email(text='john.doe@metal.ai', span=(13, 31))
        ])
