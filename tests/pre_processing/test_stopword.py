from unittest import TestCase

from soffos.pre_processing import TextSpan
from soffos.pre_processing.stopword import split_stopwords


class Tests(TestCase):
    def test_split_stopwords(self):
        text = 'The dog is derived from an ancient, extinct wolf.'
        text_spans = split_stopwords(text)
        self.assertListEqual(text_spans, [
            TextSpan(text=' dog ', span=(3, 8)),
            TextSpan(text=' derived ', span=(10, 19)),
            TextSpan(text=' ', span=(23, 24)),
            TextSpan(text=' ancient, extinct wolf.', span=(26, 49))
        ])
