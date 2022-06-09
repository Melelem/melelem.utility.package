import re

from .text import TextSpan


class Paragraph(TextSpan):
    @classmethod
    def from_text(cls, text: str):
        """
        Splits a given text into a list of paragraphs
        """
        return [
            cls(text=match.group(), span=match.span())
            for match in re.finditer(r'[\S ]+', text)
        ]
