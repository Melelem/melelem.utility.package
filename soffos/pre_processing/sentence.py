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

    @classmethod
    def _get_break_spans(cls, text: str, non_break_spans: t.List[Span]):
        punct_break_spans = [match.span() for match in re.finditer(r'[.!?]', text)]
        punct_break_spans = cls.get_non_overlapping_spans(non_break_spans, punct_break_spans)
        punct_break_spans = cls.merge_spans(punct_break_spans)

        line_break_spans = [match.span() for match in re.finditer(r'[\r\n\t\f]+', text)]
        line_break_spans = cls.get_non_overlapping_spans(non_break_spans, line_break_spans)

        return punct_break_spans, line_break_spans

    @classmethod
    def _get_split_spans(
        cls,
        text: str,
        punct_break_spans: t.List[Span],
        line_break_spans: t.List[Span]
    ):
        split_spans = line_break_spans.copy()
        for (_, span_end) in punct_break_spans:
            match = re.match(r'\s+', text[span_end:])
            if match:
                span = match.span()
                span = (span_end + span[0], span_end + span[1])
            else:
                span = (span_end, span_end)
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

        punct_break_spans, line_break_spans = cls._get_break_spans(text, non_break_spans)
        if punct_break_spans or line_break_spans:
            split_spans = cls._get_split_spans(text, punct_break_spans, line_break_spans)
            return cls.split(text, split_spans, span_offset)
        else:
            return [cls(
                text=text,
                span=(span_offset, span_offset + len(text))
            )]


def fix_truncated_text(answer: str):
    valid_sents = [s.text for s in Sentence.from_text(answer) if s.text[-1] in '.!?']
    if valid_sents:
        return ' '.join(valid_sents)
    return answer
