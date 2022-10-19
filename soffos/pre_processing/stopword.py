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


def _load_stopwords_patterns():
    return {
        language: r'\b({})\b'.format('|'.join(map(re.escape, stopwords)))
        for language, stopwords in STOPWORDS().items()
    }


STOPWORDS = LazyLoader(_load_stopwords)
STOPWORDS_PATTERNS = LazyLoader(_load_stopwords_patterns)


class Stopword(TextSpan):
    @classmethod
    def from_text(
        cls,
        text: str,
        language: str = 'english',
        ignore_case: bool = True,
        span_offset: int = 0
    ):
        pattern = STOPWORDS_PATTERNS()[language.lower()]
        matches = re.finditer(pattern, text, flags=re.IGNORECASE if ignore_case else None)
        return cls.from_matches(matches, span_offset)

    @classmethod
    def split_text(
        cls,
        text: str,
        language: str = 'english',
        ignore_case: bool = True,
        span_offset: int = 0
    ):
        stopwords = cls.from_text(text, language, ignore_case)
        spans = [stopword.span for stopword in stopwords]
        return TextSpan.split(text, spans, span_offset) if spans else []


def get_language(text: str):
    """Detect language based on the presence of stop words."""
    words = set(text.lower().split())
    lang_stopword_counts = {
        lang: len(words & stopwords)
        for lang, stopwords in STOPWORDS().items()
    }
    return max(lang_stopword_counts.items(), key=lambda item: item[1])[0]
