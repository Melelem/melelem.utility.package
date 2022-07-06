import typing as t
import json
import re

from ..utilities import LazyLoader
from .. import DATA_DIR
from .text import TextSpan, punct


def _load_abbreviations() -> t.Dict[str, str]:
    path = DATA_DIR.joinpath('abbreviations.json')
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def _load_known_abbreviations_pattern():
    pattern = '|'.join(map(re.escape, ABBREVIATIONS()))
    pattern = pattern.replace(r'\.', r'\.?')
    return r'\b(?:{})'.format(pattern)


def _load_unknown_abbreviations_pattern():
    return ''.join([
        # First letter.
        # - must be capital
        # - must be at start of line or have a space before.
        r'(?:(?<=^)|(?<= ))[A-Z]',
        # Optional period after first letter.
        r'\.?'
        # Middle letters and optional periods.
        r'(?:[a-zA-Z]*\.?)*',
        # Last letter.
        # - must be capital
        # - must be at end of line or have a space after.
        r'[A-Z](?:(?=\.?$)|(?=\.? )|(?=\.{punct}))'.format(punct=punct),
        # Optional period after last letter.
        # - must be at end of line
        # -- or must have spaces and a lowercase letter.
        # -- or must have an end-of-sentence punctuation.
        r'\.?(?:(?=$)|(?= +[a-z])|(?={punct}))'.format(punct=punct)
    ])


ABBREVIATIONS = LazyLoader(_load_abbreviations)
KNOWN_ABBREVIATIONS_PATTERN = LazyLoader(_load_known_abbreviations_pattern)
UNKNOWN_ABBREVIATIONS_PATTERN = LazyLoader(_load_unknown_abbreviations_pattern)


class Abbreviation(TextSpan):
    @classmethod
    def from_text(cls, text: str):
        # Match known abbreviations.
        matches = re.finditer(KNOWN_ABBREVIATIONS_PATTERN(), text)
        known_abbreviations = cls.from_matches(matches)

        # Match unknown abbreviations.
        matches = re.finditer(UNKNOWN_ABBREVIATIONS_PATTERN(), text, flags=re.MULTILINE)
        abbreviations = cls.from_matches(matches)

        # Get unknown abbreviations.
        unknown_abbreviations = list(set(abbreviations) - set(known_abbreviations))
        unknown_abbreviations.sort(key=lambda abbreviation: abbreviation.span)

        return known_abbreviations, unknown_abbreviations
