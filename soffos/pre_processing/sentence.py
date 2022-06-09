import typing as t
import re

from .text import TextSpan


# REGEX patterns used for text processing
ALPHABETS = r'([A-Za-z])'
PREFIXES = r'(Mr|St|Mrs|Ms|Dr)[.]'
SUFFIXES = r'(Inc|Ltd|Jr|Sr|Co)'
STARTERS = r'(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s' \
    r'|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)'
ACRONYMS = r'([A-Z][.][A-Z][.](?:[A-Z][.])?)'
WEBSITES = r'[.](com|net|org|io|gov)'


class Sentence(TextSpan):
    @property
    def is_title(self):
        return self.text.istitle()

    @classmethod
    def from_text(cls, text: str, span_offset: int = 0):
        """
        Splits a given text into a list of sentences
        """
        text = ' ' + text + '  '
        text = text.replace('\n', ' ')
        text = re.sub(PREFIXES, '\\1<prd>', text)
        text = re.sub(WEBSITES, '<prd>\\1', text)

        if 'Ph.D' in text:
            text = text.replace('Ph.D.', 'Ph<prd>D<prd>')

        text = re.sub(r'\s' + ALPHABETS + '[.] ', ' \\1<prd> ', text)
        text = re.sub(ACRONYMS + ' ' + STARTERS, '\\1<stop> \\2', text)
        text = re.sub(ALPHABETS + '[.]' + ALPHABETS + '[.]' + ALPHABETS + '[.]',
                      '\\1<prd>\\2<prd>\\3<prd>', text)
        text = re.sub(ALPHABETS + '[.]' + ALPHABETS +
                      '[.]', '\\1<prd>\\2<prd>', text)
        text = re.sub(' ' + SUFFIXES + '[.] ' + STARTERS, ' \\1<stop> \\2', text)
        text = re.sub(' ' + SUFFIXES + '[.]', ' \\1<prd>', text)
        text = re.sub(' ' + ALPHABETS + '[.]', ' \\1<prd>', text)

        if '”' in text:
            text = text.replace('.”', '”.')
        if '"' in text:
            text = text.replace('."', '".')
        if '!' in text:
            text = text.replace('!"', '"!')
        if '?' in text:
            text = text.replace('?"', '"?')

        text = text.replace('.', '.<stop>')
        text = text.replace('?', '?<stop>')
        text = text.replace('!', "!<stop>")
        text = text.replace('<prd>', '.')

        # sentences = text.split('<stop>')
        # sentences = sentences[:-1]
        # sentences = [s.strip() for s in sentences]

        sentences: t.List[cls] = []
        last_match_span_end = 0
        for match in re.finditer(r'(<stop>)?[ ]*(.+?)(?=<stop>)', text):
            span = match.span()
            sentence = cls(
                text=match.group(2),
                span=(span_offset + span[0], span_offset + span[1])
            )
            last_match_span_end = sentence.span[1]
            sentences.append(sentence)
        if last_match_span_end < len(text):
            text = text[last_match_span_end:]\
                .replace('<stop>', '')\
                .strip()
            if text:
                sentence = cls(
                    text=text,
                    span=(span_offset + last_match_span_end, span_offset + len(text))
                )
                sentences.append(sentence)

        return sentences
