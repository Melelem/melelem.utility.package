import typing as t
from dataclasses import dataclass
import string
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

punct = r'[{}]'.format(string.punctuation)
not_punct = r'[^{}]'.format(string.punctuation)

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

    @classmethod
    def split(cls, text: str, spans: t.List[Span], span_offset: int = 0):
        """Split text on the spans provided. The surrounding text_spans are returned.

        :param text: The text to split
        :param spans: Lists where the text is split
        :param span_offset: Offset all spans returned (useful if text is subtext), defaults to 0
        :return: The surrounding text spans
        """
        spans.sort()
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
    def from_matches(cls, matches: t.Iterator[re.Match]):
        return [
            cls(text=match.group(), span=match.span())
            for match in matches
        ]


def split_punctuations(text: str, span_offset: int = 0):
    text_spans: t.List[TextSpan] = []
    for match in re.finditer(not_punct + r'+', text):
        span = match.span()
        text_spans.append(TextSpan(
            text=match.group(),
            span=(span_offset + span[0], span_offset + span[1])
        ))

    return text_spans


def remove_punctuations(text: str):
    return text.translate(str.maketrans('', '', string.punctuation))


def replace_newlines(text: str, replacement: str = ' '):
    return re.sub(r'[\r|\n|\r\n]+', replacement, text)


def replace_excessive_spaces(text: str):
    return re.sub(r'[ ]{2,}', ' ', text)


def replace_brackets(text: str, replacement: str = ''):
    return re.sub(r'( )?[\(\[].*?[\)\]]', replacement, text)


def replace_special_chars(text: str, replacement: str = ''):
    return re.sub(r'[^a-zA-Z0-9.,!?/:;\"\'\s]', replacement, text)


def normalize_chars(text: str, encoding: str = 'ascii', errors: str = 'ignore'):
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

    # replace multiple consecutive white spaces with just one
    text = re.sub(r'\s+', ' ', text)

    return text
