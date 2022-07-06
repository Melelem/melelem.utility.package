import re

from .text import TextSpan


class Paragraph(TextSpan):
    @classmethod
    def from_text(cls, text: str):
        """
        Splits a given text into a list of paragraphs
        """
        matches = re.finditer(r'[\S ]+', text)
        return cls.from_matches(matches)
