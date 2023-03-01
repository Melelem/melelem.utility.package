import typing as t
from dataclasses import dataclass
import json
import re

from ..utilities import LazyLoader
from .. import DATA_DIR


def _load_char_substitutions() -> t.Dict[str, t.Set[str]]:
    char_substitutions_path = DATA_DIR.joinpath('character_substitutions.json')
    with open(char_substitutions_path, 'r', encoding='utf-8') as char_substitutions_file:
        return {
            char.upper(): set(substitutions)
            for char, substitutions in json.load(char_substitutions_file).items()
        }


def _load_char_substitution_patterns():
    return {
        char: r'(?:{})'.format('|'.join([char, char.lower()] + list(map(re.escape, subs))))
        for char, subs in CHAR_SUBSTITUTIONS().items()
    }


CHAR_SUBSTITUTIONS = LazyLoader(_load_char_substitutions)
CHAR_SUBSTITUTION_PATTERNS = LazyLoader(_load_char_substitution_patterns)


Span = t.Tuple[int, int]


@dataclass(frozen=True)
class TextSpan:
    text: str
    span: Span

    @property
    def length(self):
        return len(self.text)

    @property
    def span_start(self):
        return self.span[0]

    @property
    def span_end(self):
        return self.span[1]

    @property
    def words(self):
        words = re.split(r'\W+', self.text)
        if words:
            words = words[1 if words[0] == '' else 0:]
        if words:
            words = words[:-1 if words[-1] == '' else len(words)]
        return words

    @staticmethod
    def merge_spans(spans: t.List[Span]):
        spans = spans.copy()
        merged_spans: t.List[Span] = []
        while spans:
            span = spans.pop(0)
            span_index = 0
            while span_index < len(spans):
                next_span = spans[span_index]
                if (
                    next_span[0] <= span[0] <= next_span[1]
                    or next_span[0] <= span[1] <= next_span[1]
                ):
                    span = (
                        span[0] if span[0] <= next_span[0] else next_span[0],
                        span[1] if span[1] >= next_span[1] else next_span[1]
                    )
                    spans.pop(span_index)
                    span_index = 0
                else:
                    span_index += 1
            merged_spans.append(span)
        merged_spans.sort()
        return merged_spans

    @classmethod
    def split(cls, text: str, spans: t.List[Span], span_offset: int = 0):
        """Split text on the spans provided. The surrounding text_spans are returned.

        :param text: The text to split
        :param spans: Lists where the text is split
        :param span_offset: Offset all spans returned (useful if text is subtext), defaults to 0
        :return: The surrounding text spans
        """
        spans = cls.merge_spans(spans)
        text_spans: t.List[cls] = []
        for span_1, span_2 in zip([None] + spans, spans + [None]):
            if span_1 is None:
                span_start = 0
                span_end = span_2[0]
            elif span_2 is None:
                span_start = span_1[1]
                span_end = len(text)
            else:
                span_start = span_1[1]
                span_end = span_2[0]
            if span_start != span_end:
                text_spans.append(cls(
                    text=text[span_start:span_end],
                    span=(span_offset + span_start, span_offset + span_end)
                ))
        return text_spans

    @classmethod
    def from_matches(cls, matches: t.Iterator[re.Match], span_offset: int = 0):
        return [
            cls(
                text=match.group(),
                span=(span_offset + match.span()[0], span_offset + match.span()[1])
            )
            for match in matches
        ]

    @staticmethod
    def get_non_overlapping_spans(spans: t.List[Span], possibly_overlapping_spans: t.List[Span]):
        return [
            possibly_overlapping_span
            for possibly_overlapping_span in possibly_overlapping_spans
            if all(
                possibly_overlapping_span[0] >= span[1]
                or possibly_overlapping_span[1] <= span[0]
                for span in spans
            )
        ]


def remove_possessions(text: str):
    return re.sub(r'(?<=\w)\'s', '', text)


def replace_newlines(text: str, replacement: str = ' '):
    return re.sub(r'[\r|\n|\r\n]+', replacement, text)


def replace_excessive_spaces(text: str):
    return re.sub(r'[ ]{2,}', ' ', text)


def replace_brackets(text: str, replacement: str = ''):
    return re.sub(r'( )?[\(\[].*?[\)\]]', replacement, text)


def replace_special_chars(text: str, replacement: str = ''):
    return re.sub(r'[^a-zA-Z0-9.,!?/:;\"\'\s]', replacement, text)


def normalize_chars(text: str, encoding: str = 'utf-8', errors: str = 'ignore'):
    text = re.sub(r'\x0d|\x1b|\x07|\uf0b7|\uf020|\u202f|\x02|(\(cid:\d+\))', '', text)

    # whitespaces
    text = re.sub(r'\x0c|\x0b|\xa0|\x09', ' ', text)

    # normalize apostrophes
    text = re.sub(r"\u201c|\u201d", "\"", text)
    text = re.sub(r'“|”', '"', text)
    text = re.sub(r'‘|’', '\'', text)
    text = re.sub(r'\'\'', '"', text)
    text = re.sub(r'``', '"', text)
    text = re.sub(r'–', '-', text)

    return text.encode(encoding, errors).decode(encoding, errors)


def normalize_whitespaces(text: str):
    text = text.strip()

    # Replace multiple consecutive spaces and tabs with just one space
    text = re.sub(r'[ |\t]{2,}', ' ', text)
    # Replace multiple consecutive new lines with just 2
    # Single and double new lines are important formatting information on which
    # certain pre-processing rules rely. (e.g. identifying non breaking periods
    # on numbered lists)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def remove_question_mark(question: str):
    return question.replace('?', '')
