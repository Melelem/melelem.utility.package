import re

from .text import TextSpan


EMAIL_PATTERN = r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*"


class Email(TextSpan):
    @classmethod
    def from_text(cls, text: str):
        """Get email spans from a body of text.

        :param text: Text to get emails from
        :return: List of email spans
        """
        matches = re.finditer(EMAIL_PATTERN, text)
        return cls.from_matches(matches)


def replace_emails(text: str, replacement: str = 'email'):
    # NOTE: https://www.w3resource.com/javascript/form/email-validation.php
    return re.sub(EMAIL_PATTERN, replacement, text)
