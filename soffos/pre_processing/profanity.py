import typing as t
import json
import re

from ..utilities import LazyLoader
from .. import DATA_DIR
from .text import TextSpan, CHAR_SUBSTITUTION_PATTERNS


def _load_profanities() -> t.Set[str]:
    profanities_path = DATA_DIR.joinpath('profanities.json')
    with open(profanities_path, 'r', encoding='utf-8') as profanities_file:
        return set(json.load(profanities_file))


def _load_profanity_patterns():
    profanity_patterns: t.Set[str] = set()
    for profanity in PROFANITIES():
        char_patterns = []
        for char in profanity:
            char_pattern = CHAR_SUBSTITUTION_PATTERNS().get(char.upper())
            if char_pattern is None:
                char_pattern = r' +' if char == ' ' else char
            char_patterns.append(char_pattern)
        profanity_pattern = r'\b{}\b'.format(''.join(char_patterns))
        profanity_patterns.add(profanity_pattern)
    return profanity_patterns


PROFANITIES = LazyLoader(_load_profanities)
PROFANITY_PATTERNS = LazyLoader(_load_profanity_patterns)


def get_profanities(text: str):
    return [
        TextSpan(text=match.group(), span=match.span())
        for profanity_pattern in PROFANITY_PATTERNS()
        for match in re.finditer(profanity_pattern, text)
    ]
