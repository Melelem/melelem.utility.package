import typing as t
from functools import reduce
import re

from .text import TextSpan, Span
from .abbreviation import get_abbreviations
from .url import get_urls


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
    def from_text(cls, text: str):
        # Get non break text spans.
        known_abbreviations, unknown_abbreviations = get_abbreviations(text)
        urls = get_urls(text)

        non_break_spans = cls._reduce_non_break_spans(
            known_abbreviations,
            unknown_abbreviations,
            urls
        )
        break_indicies = cls._get_break_indicies(text, non_break_spans)
        split_spans = cls._get_split_spans(text, break_indicies)
        return cls.split(text, split_spans)
