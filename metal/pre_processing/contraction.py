import typing as t
import json
import re

from ..utilities import LazyLoader
from .. import DATA_DIR


def _load_contractions() -> t.Dict[str, str]:
    contractions_path = DATA_DIR.joinpath('contractions.json')
    with open(contractions_path, 'r', encoding='utf-8') as contractions_file:
        return json.load(contractions_file)


CONTRACTIONS = LazyLoader(_load_contractions)


def expand_contractions(
    text: str,
    contractions: t.Dict[str, str] = None,
    ignore_case: bool = True
):
    if contractions is None:
        contractions = CONTRACTIONS()
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
