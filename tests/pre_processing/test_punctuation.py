from unittest import TestCase

from soffos.pre_processing import TextSpan
from soffos.pre_processing.punctuation import (
    Punctuation,
    split_punctuations
)


class PunctuationTests(TestCase):
    def test_from_text(self):
        text = 'Hello. Why? No! ;#$%^&*()_+=-'
        punctuations = Punctuation.from_text(text)
        self.assertListEqual(punctuations, [
            Punctuation(text='.', span=(5, 6)),
            Punctuation(text='?', span=(10, 11)),
            Punctuation(text='!', span=(14, 15)),
            Punctuation(text=';', span=(16, 17)),
            Punctuation(text='#', span=(17, 18)),
            Punctuation(text='$', span=(18, 19)),
            Punctuation(text='%', span=(19, 20)),
            Punctuation(text='^', span=(20, 21)),
            Punctuation(text='&', span=(21, 22)),
            Punctuation(text='*', span=(22, 23)),
            Punctuation(text='(', span=(23, 24)),
            Punctuation(text=')', span=(24, 25)),
            Punctuation(text='_', span=(25, 26)),
            Punctuation(text='+', span=(26, 27)),
            Punctuation(text='=', span=(27, 28)),
            Punctuation(text='-', span=(28, 29))
        ])


class Tests(TestCase):
    def test_split_punctuations(self):
        text = 'The `dog` is derived from an ancient, extinct wolf.'
        text_spans = split_punctuations(text)

        expected_text_spans = []
        for subtext in ['The ', 'dog', ' is derived from an ancient', ' extinct wolf']:
            index = text.index(subtext)
            expected_text_spans.append(TextSpan(
                text=subtext, span=(index, index + len(subtext))
            ))
        self.assertListEqual(text_spans, expected_text_spans)
