import typing as t
from functools import reduce
import re

from .text import TextSpan, Span
from .abbreviation import Abbreviation
from .email import Email
from .url import Url


class Sentence(TextSpan):
    @property
    def is_title(self):
        return self.text.istitle()

    @staticmethod
    def _reduce_non_break_spans(*text_span_lists: t.List[TextSpan]):
        def get_spans(spans: t.List[Span], text_spans: t.List[TextSpan]):
            return spans + [text_span.span for text_span in text_spans]
        return reduce(get_spans, text_span_lists, [])

    @staticmethod
    def _get_break_indicies(text: str, non_break_spans: t.List[Span]):
        break_indicies: t.List[int] = []
        for match in re.finditer(r'[.!?]', text):
            i = match.span()[0]
            if all(i < span[0] or i > span[1] for span in non_break_spans):
                break_indicies.append(i)
        return break_indicies

    @staticmethod
    def _get_split_spans(text: str, break_indicies: t.List[int]):
        split_spans: t.List[Span] = []
        for i in break_indicies:
            i += 1
            span = (i, i)
            match = re.match(r'\s+', text[i:])
            if match:
                span = match.span()
                span = (i + span[0], i + span[1])
            split_spans.append(span)
        return split_spans

    @classmethod
    def from_text(cls, text: str, span_offset: int = 0):
        """Split text into sentences by identifying sentence-breaking punctuations.

        :param text: The text to split into sentences
        :param span_offset: Offset all spans returned (useful if text is subtext), defaults to 0
        :return: List of sentence spans
        """
        # Get non break text spans.
        known_abbreviations, unknown_abbreviations = Abbreviation.from_text(text)
        urls = Url.from_text(text)
        emails = Email.from_text(text)

        non_break_spans = cls._reduce_non_break_spans(
            known_abbreviations,
            unknown_abbreviations,
            urls,
            emails
        )
        break_indicies = cls._get_break_indicies(text, non_break_spans)
        split_spans = cls._get_split_spans(text, break_indicies)
        return cls.split(text, split_spans, span_offset)
