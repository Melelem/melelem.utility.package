import typing as t
import os
import re

from ..utilities import LazyLoader
from .. import DATA_DIR
from .text import TextSpan


def _load_stopwords():
    """Get stopwords for each supported language."""
    stopwords: t.Dict[str, t.Set[str]] = {}
    stopwords_path = DATA_DIR.joinpath('stopwords')
    for file_name in os.listdir(stopwords_path):
        file_path = stopwords_path.joinpath(file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            stopwords[file_name] = set(file.read().splitlines())
    return stopwords


STOPWORDS = LazyLoader(_load_stopwords)


def split_stopwords(
    text: str,
    language: str = 'english',
    ignore_case: bool = True,
    span_offset: int = 0
):
    stopwords = STOPWORDS()[language.lower()]
    pattern = r'\b(' + '|'.join(map(re.escape, stopwords)) + r')\b'

    index = 0
    text_spans: t.List[TextSpan] = []
    for match in re.finditer(pattern, text, flags=re.IGNORECASE if ignore_case else None):
        span = match.span()
        if span[0] > 0:
            text_spans.append(TextSpan(
                text=text[index:span[0]],
                span=(span_offset + index, span_offset + span[0])
            ))
        index = span[1]

    text_length = len(text)
    if index < text_length:
        text_spans.append(TextSpan(
            text=text[index:text_length],
            span=(span_offset + index, span_offset + text_length)
        ))

    return text_spans


def get_language(text: str):
    """Detect language based on the presence of stop words."""
    words = set(text.lower().split())
    lang_stopword_counts = {
        lang: len(words & stopwords)
        for lang, stopwords in STOPWORDS().items()
    }
    return max(lang_stopword_counts.items(), key=lambda item: item[1])[0]
