from unittest import TestCase

from melelem.pre_processing.email import Email


class EmailTests(TestCase):
    def test_from_text(self):
        text = 'His email is john.doe@melelem.ai.'
        emails = Email.from_text(text)
        self.assertListEqual(emails, [
            Email(text='john.doe@melelem.ai', span=(13, 31))
        ])
