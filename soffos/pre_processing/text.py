import typing as t
from dataclasses import dataclass
import string
import json
import re

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk

from ..utilities import LazyLoader
from .. import DATA_DIR


# --------------------------------------------------------------------------------------------------
# Global variables.
# --------------------------------------------------------------------------------------------------

def load_stopwords() -> t.Dict[str, t.Set[str]]:
    # Get stopwords for each supported language.
    nltk.download('stopwords', download_dir=DATA_DIR.joinpath('nltk'))
    return {
        lang: set(stopwords.words(lang))
        for lang in stopwords.fileids()
    }


def load_contractions() -> t.Dict[str, str]:
    contractions_path = DATA_DIR.joinpath('contractions.json')
    with open(contractions_path, 'r', encoding='utf-8') as contractions_file:
        return json.load(contractions_file)


def load_char_substitutions() -> t.Dict[str, t.Set[str]]:
    char_substitutions_path = DATA_DIR.joinpath('character_substitutions.json')
    with open(char_substitutions_path, 'r', encoding='utf-8') as char_substitutions_file:
        return {
            char.upper(): set(substitutions)
            for char, substitutions in json.load(char_substitutions_file).items()
        }


def load_char_substitution_patterns():
    return {
        char: r'(?:{})'.format('|'.join([char, char.lower()] + list(map(re.escape, subs))))
        for char, subs in CHAR_SUBSTITUTIONS.lazy_load().items()
    }


def load_profanities() -> t.Set[str]:
    profanities_path = DATA_DIR.joinpath('profanities.json')
    with open(profanities_path, 'r', encoding='utf-8') as profanities_file:
        return set(json.load(profanities_file))


def load_profanity_patterns():
    profanity_patterns: t.Set[str] = set()
    for profanity in PROFANITIES.lazy_load():
        char_patterns = []
        for char in profanity:
            char_pattern = CHAR_SUBSTITUTION_PATTERNS.lazy_load().get(char.upper())
            if char_pattern is None:
                char_pattern = r' +' if char == ' ' else char
            char_patterns.append(char_pattern)
        profanity_pattern = r'\b{}\b'.format(''.join(char_patterns))
        profanity_patterns.add(profanity_pattern)
    return profanity_patterns


STOPWORDS = LazyLoader(load_stopwords)
CONTRACTIONS = LazyLoader(load_contractions)
CHAR_SUBSTITUTIONS = LazyLoader(load_char_substitutions)
CHAR_SUBSTITUTION_PATTERNS = LazyLoader(load_char_substitution_patterns)
PROFANITIES = LazyLoader(load_profanities)
PROFANITY_PATTERNS = LazyLoader(load_profanity_patterns)


# --------------------------------------------------------------------------------------------------
# Data classes and processing functions.
# --------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class TextSpan:
    text: str
    span: t.Tuple[int, int]

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
    def split(cls, text: str, spans: t.List[t.Tuple[int, int]]):
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
                    span=(span_start, span_end)
                ))
        return text_spans


def split_punctuations(text: str, span_offset: int = 0):
    pattern = r'[^' + string.punctuation + r']+'

    text_spans: t.List[TextSpan] = []
    for match in re.finditer(pattern, text):
        span = match.span()
        text_spans.append(TextSpan(
            text=match.group(),
            span=(span_offset + span[0], span_offset + span[1])
        ))

    return text_spans


def split_stopwords(
    text: str,
    language: str = 'english',
    ignore_case: bool = True,
    span_offset: int = 0
):
    stopwords = STOPWORDS.lazy_load()[language.lower()]
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


def get_profanities(text: str):
    return [
        TextSpan(text=match.group(), span=match.span())
        for profanity_pattern in PROFANITY_PATTERNS.lazy_load()
        for match in re.finditer(profanity_pattern, text)
    ]


def remove_punctuations(text: str):
    return text.translate(str.maketrans('', '', string.punctuation))


def expand_contractions(
    text: str,
    contractions: t.Dict[str, str] = None,
    ignore_case: bool = True
):
    if contractions is None:
        contractions = CONTRACTIONS.lazy_load()
    pattern = (
        r'(?:(?<=^)|(?<= ))'
        + f"({'|'.join(map(re.escape, contractions.keys()))})"
        + r'(?:(?=$)|(?= )|(?=\.))'
    )
    flags = re.MULTILINE
    if ignore_case:
        flags |= re.IGNORECASE
        contractions = {
            contraction.lower(): expansion
            for contraction, expansion in contractions.items()
        }

    def expand_contraction(match: re.Match):
        contraction: str = match.group()
        contraction = contraction.lower() if ignore_case else contraction
        expansion = contractions[contraction]
        if contraction[0].isupper() and expansion[1].islower():
            expansion = expansion[0].upper() + expansion[1:]
        return expansion

    return re.compile(pattern, flags).sub(expand_contraction, text)


def strip_html_tags(text: str):
    return BeautifulSoup(text, 'html.parser').get_text()


def remove_non_ascii_chars(text: str):
    """Remove non-ascii characters from text."""
    return text.encode('ascii', 'ignore').decode()


def get_language(text: str):
    """Detect language based on the presence of stop words."""
    words = set(nltk.wordpunct_tokenize(text.lower()))
    lang_stopword_counts = {
        lang: len(words & stopwords)
        for lang, stopwords in STOPWORDS.lazy_load().items()
    }
    return max(lang_stopword_counts.items(), key=lambda item: item[1])[0]


def replace_emails(text: str, replacement: str = 'email'):
    # NOTE: https://www.w3resource.com/javascript/form/email-validation.php
    return re.sub(r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*", replacement, text)


def replace_urls(text: str, replacement: str = 'url'):
    return re.sub(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", replacement, text)


def replace_newlines(text: str, replacement: str = ' '):
    return re.sub(r'[\r|\n|\r\n]+', replacement, text)


def replace_excessive_spaces(text: str):
    return re.sub(r'[ ]{2,}', ' ', text)


def replace_brackets(text: str, replacement: str = ''):
    return re.sub(r'( )?[\(\[].*?[\)\]]', replacement, text)


def replace_special_chars(text: str, replacement: str = ''):
    return re.sub(r'[^a-zA-Z0-9.,!?/:;\"\'\s]', replacement, text)
