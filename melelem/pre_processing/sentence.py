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
    def _get_sent_boundaries(cls, text: str, non_break_spans: t.List[Span], line_break_split=False):
        punct_break_spans = [match.span() for match in re.finditer(r'[.!?]', text)]
        punct_break_spans = cls.get_non_overlapping_spans(non_break_spans, punct_break_spans)
        punct_break_spans = cls.merge_spans(punct_break_spans)
        
        line_break_spans = None
        if line_break_split:
            line_break_spans = [match.span() for match in re.finditer(r'[\r\n\t\f]+', text)]
            line_break_spans = cls.get_non_overlapping_spans(non_break_spans, line_break_spans)

        return punct_break_spans, line_break_spans

    @classmethod
    def _get_split_spans(
        cls,
        text: str,
        punct_sent_boundaries: t.List[Span],
        line_sent_boundaries: t.List[Span] = None
    ):
        split_spans = []
        if line_sent_boundaries:
            split_spans = line_sent_boundaries.copy()
        for (_, span_end) in punct_sent_boundaries:
            match = re.match(r'\s+', text[span_end:])
            if match:
                span = match.span()
                span = (span_end + span[0], span_end + span[1])
            else:
                span = (span_end, span_end)
            split_spans.append(span)
        return split_spans

    @classmethod
    def from_text(cls, text: str, span_offset: int = 0, line_break_split=False):
        """Split text into sentences by identifying sentence-breaking punctuations.

        :param text: The text to split into sentences
        :param span_offset: Offset all spans returned (useful if text is subtext), defaults to 0
        :param line_break_split: Whether to consider line breaks as sentence boundaries
        :return: List of sentence spans
        """
        # Get non break text spans.
        known_abbreviations, unknown_abbreviations = Abbreviation.from_text(text, for_segmentation=True)
        urls = Url.from_text(text)
        emails = Email.from_text(text)
        floating_point_numbers = TextSpan.from_matches(re.finditer(r'\b(?:\d+\.\d+)', text))
        numbered_lists = TextSpan.from_matches(re.finditer(r'(?:\n[\d|A-Za-z]{1,3})(\.)', text))
        non_break_spans = cls._reduce_non_break_spans(
            known_abbreviations,
            unknown_abbreviations,
            urls,
            emails,
            floating_point_numbers,
            numbered_lists
        )

        punct_sent_boundaries, line_sent_boundaries = cls._get_sent_boundaries(text, non_break_spans, line_break_split)
        if punct_sent_boundaries or line_sent_boundaries:
            split_spans = cls._get_split_spans(text, punct_sent_boundaries, line_sent_boundaries)
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
