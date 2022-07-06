from unittest import TestCase

from soffos.pre_processing.email import Email


class EmailTests(TestCase):
    def test_from_text(self):
        text = 'His email is john.doe@soffos.ai.'
        emails = Email.from_text(text)
        self.assertListEqual(emails, [
            Email(text='john.doe@soffos.ai', span=(13, 31))
        ])
