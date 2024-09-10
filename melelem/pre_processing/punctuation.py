import typing as t
import string
import re

from .text import TextSpan


punct = r'[{}]'.format(string.punctuation)
not_punct = r'[^{}]'.format(string.punctuation)


class Punctuation(TextSpan):
    @classmethod
    def from_text(cls, text: str):
        matches = re.finditer(punct, text)
        return cls.from_matches(matches)


def split_punctuations(text: str, span_offset: int = 0):
    pattern = r'{not_punct}+'.format(not_punct=not_punct)
    text_spans: t.List[TextSpan] = []
    for match in re.finditer(pattern, text):
        span = match.span()
        text_spans.append(TextSpan(
            text=match.group(),
            span=(span_offset + span[0], span_offset + span[1])
        ))

    return text_spans


def remove_punctuations(text: str):
    return text.translate(str.maketrans('', '', string.punctuation))
