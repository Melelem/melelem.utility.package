import typing as t
import json
import re

from ..utilities import LazyLoader
from .. import DATA_DIR
from .text import TextSpan
from .punctuation import punct

# To simply find abbreviations.
###
def _load_abbreviations() -> t.Dict[str, str]:
    path = DATA_DIR.joinpath('abbreviations.json')
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def _load_known_abbreviations_pattern():
    pattern = '|'.join(map(re.escape, ABBREVIATIONS()))
    #NOTE: Why making the dot optional? This matches subwords. In the case of sentence splitting, the reason we try to find them is specifically for that dot.
    pattern = pattern.replace(r'\.', r'\.?')
    return r'\b(?:{})'.format(pattern)


def _load_unknown_abbreviations_pattern():
    #NOTE: string.punctuation contains all punctuations, not just end-of-sentence punctuation. 
    # Only . ! ? are end-of-sentence, and maybe some others in rare cases.
    return (
        # First letter.
        # - must be capital
        # - must be at start of line or have a space before.
        r'(?:(?<=^)|(?<= ))[A-Z]'
        # Optional period after first letter.
        r'\.?'
        # Middle letters and optional periods.
        r'(?:[a-zA-Z]*\.?)*'
        # Last letter.
        # - must be capital
        # - must be at end of line or have a space after.
        r'[A-Z](?:(?=\.?$)|(?=\.? )|(?=\.{punct}))'
        # Optional period after last letter.
        # - must be at end of line
        # -- or must have spaces and a lowercase letter.
        # -- or must have an end-of-sentence punctuation.
        r'\.?(?:(?=$)|(?= +[a-z])|(?={punct}))'
    ).format(punct=punct)
###


# For sentence segmentations.
###
def _load_abbreviations_for_segmentation() -> t.Dict[str, str]:
    path = DATA_DIR.joinpath('abbreviations.json')
    with open(path, 'r', encoding='utf-8') as file:
        abbreviations = json.load(file)
    
    # On some cases, some abbreviations act as end of sentence too.
    # Determining this when the next letter is capital, only for abbreviations which usually occur at the end of sentence.
    end_of_sent_condition_pattern = r"(?!\s{1,}[A-Z])"
    cases = ["et al.", "etc."]
    adjusted_abbreviations = {}
    for a in abbreviations:
        if a in cases:
            adjusted_abbreviations[a+end_of_sent_condition_pattern] = abbreviations[a]
        else:
            adjusted_abbreviations[a] = abbreviations[a]

    return adjusted_abbreviations


def _load_known_abbreviations_pattern_for_segmentation():
    pattern = '|'.join(map(re.escape, ABBREVIATIONS_FOR_SEGMENTATION()))
    return r'\b(?:{})'.format(pattern)


def _load_unknown_abbreviations_pattern_for_segmentation():
    return r"(?:[a-zA-Z]\.){2,}(?!\s{1,}[A-Z])"
###


ABBREVIATIONS = LazyLoader(_load_abbreviations)
KNOWN_ABBREVIATIONS_PATTERN = LazyLoader(_load_known_abbreviations_pattern)
UNKNOWN_ABBREVIATIONS_PATTERN = LazyLoader(_load_unknown_abbreviations_pattern)
ABBREVIATIONS_FOR_SEGMENTATION = LazyLoader(_load_abbreviations_for_segmentation)
KNOWN_ABBREVIATIONS_PATTERN_FOR_SEGMENTATION = LazyLoader(_load_known_abbreviations_pattern_for_segmentation)
UNKNOWN_ABBREVIATIONS_PATTERN_FOR_SEGMENTATION = LazyLoader(_load_unknown_abbreviations_pattern_for_segmentation)

class Abbreviation(TextSpan):
    @classmethod
    def from_text(cls, text: str, for_segmentation=False):
        # For sentence splitting, to deal with abbreviations which end with a period that is also acting as a sentence boundary.
        if for_segmentation:
            # Match known abbreviations.
            matches = re.finditer(KNOWN_ABBREVIATIONS_PATTERN_FOR_SEGMENTATION(), text)
            known_abbreviations = cls.from_matches(matches)

            # Match unknown abbreviations.
            matches = re.finditer(UNKNOWN_ABBREVIATIONS_PATTERN_FOR_SEGMENTATION(), text, flags=re.MULTILINE)
            abbreviations = cls.from_matches(matches)

            # Get unknown abbreviations.
            unknown_abbreviations = list(set(abbreviations) - set(known_abbreviations))
            unknown_abbreviations.sort(key=lambda abbreviation: abbreviation.span)
        else:
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
