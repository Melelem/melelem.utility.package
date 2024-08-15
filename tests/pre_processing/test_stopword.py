from unittest import TestCase

from metal.pre_processing import TextSpan
from metal.pre_processing.stopword import Stopword


class StopwordTests(TestCase):
    def test_from_text(self):
        text = 'The dog is derived from an ancient, extinct wolf.'
        stopwords = Stopword.from_text(text)
        self.assertListEqual(stopwords, [
            Stopword(text='The', span=(0, 3)),
            Stopword(text='is', span=(8, 10)),
            Stopword(text='from', span=(19, 23)),
            Stopword(text='an', span=(24, 26))
        ])

    def test_split_text(self):
        text = 'The dog is derived from an ancient, extinct wolf.'
        non_stopwords = Stopword.split_text(text)
        self.assertListEqual(non_stopwords, [
            TextSpan(text=' dog ', span=(3, 8)),
            TextSpan(text=' derived ', span=(10, 19)),
            TextSpan(text=' ', span=(23, 24)),
            TextSpan(text=' ancient, extinct wolf.', span=(26, 49))
        ])
