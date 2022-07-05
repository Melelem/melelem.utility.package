import typing as t
from unittest import TestCase

from soffos.pre_processing.text import (
    load_stopwords,
    TextSpan,
    split_punctuations,
    split_stopwords,
    get_profanities,
    get_abbreviations
)


class TextSpanTests(TestCase):
    def test_split(self):
        text = 'The dog is derived from an ancient, extinct wolf.'
        text_spans = TextSpan.split(text, spans=[(24, 26), (0, 3)])
        self.assertListEqual(text_spans, [
            TextSpan(text=' dog is derived from ', span=(3, 24)),
            TextSpan(text=' ancient, extinct wolf.', span=(26, len(text)))
        ])


class Tests(TestCase):
    def test_load_stopwords(self):
        stopwords = load_stopwords()
        self.assertIsInstance(stopwords, dict)

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

    def test_split_stopwords(self):
        text = 'The dog is derived from an ancient, extinct wolf.'
        text_spans = split_stopwords(text)
        self.assertListEqual(text_spans, [
            TextSpan(text=' dog ', span=(3, 8)),
            TextSpan(text=' derived ', span=(10, 19)),
            TextSpan(text=' ', span=(23, 24)),
            TextSpan(text=' ancient, extinct wolf.', span=(26, 49))
        ])

    def test_get_profanities(self):
        # Normal casing.
        text_spans = get_profanities('He is a bitch, she said.')
        self.assertListEqual(text_spans, [TextSpan(text='bitch', span=(8, 13))])

        # Mixed casing.
        text_spans = get_profanities('He is a BitCh, she said.')
        self.assertListEqual(text_spans, [TextSpan(text='BitCh', span=(8, 13))])

        # Character substituion.
        text_spans = get_profanities('He is a b!tCh, she said.')
        self.assertListEqual(text_spans, [TextSpan(text='b!tCh', span=(8, 13))])

        # Irregular spacing.
        text_spans = get_profanities('dry     hump')
        self.assertListEqual(text_spans, [TextSpan(text='dry     hump', span=(0, 12))])

        # Conjunction. NOTE: 'ass' should not be matched
        text_spans = get_profanities('asshole')
        self.assertListEqual(text_spans, [TextSpan(text='asshole', span=(0, 7))])


class AbbreviationTests(TestCase):

    class TestData(t.NamedTuple):
        text: str
        known: t.List[str] = []
        unknown: t.List[str] = []

    def assert_abbreviations(self, *datas: TestData):
        for data in datas:
            known_abbreviations, unknown_abbreviations = get_abbreviations(data.text)

            expected_known_abbreviations = []
            for known_abbreviation in data.known:
                index = data.text.index(known_abbreviation)
                expected_known_abbreviations.append(TextSpan(
                    text=known_abbreviation,
                    span=(index, index + len(known_abbreviation))
                ))
            self.assertListEqual(known_abbreviations, expected_known_abbreviations)

            expected_unknown_abbreviations = []
            for unknown_abbreviation in data.unknown:
                index = data.text.index(unknown_abbreviation)
                expected_unknown_abbreviations.append(TextSpan(
                    text=unknown_abbreviation,
                    span=(index, index + len(unknown_abbreviation))
                ))
            self.assertListEqual(unknown_abbreviations, expected_unknown_abbreviations)

    def test(self):
        text = 'Prof. John has a Ph.D. in computer science and is experienced in OOP.'
        known_abbreviations, unknown_abbreviations = get_abbreviations(text)
        self.assertListEqual(known_abbreviations, [
            TextSpan(text='Prof.', span=(0, 5)),
            TextSpan(text='Ph.D.', span=(17, 22)),
        ])
        self.assertListEqual(unknown_abbreviations, [
            TextSpan(text='OOP.', span=(65, 69))
        ])

    def test_known__mixed_periods(self):
        for text in ['Ph.D.', 'PhD.', 'PhD']:
            known_abbreviations, _ = get_abbreviations(text)
            self.assertListEqual(known_abbreviations, [
                TextSpan(text=text, span=(0, len(text)))
            ])

    def test_unkown__start_boundaries(self):
        self.assert_abbreviations(
            self.TestData(text='ABC blah blah.', unknown=['ABC']),  # start of paragraph.
            self.TestData(text='blah.\nABC blah.', unknown=['ABC']),  # start of new paragraph.
            self.TestData(text='blah. ABC blah.', unknown=['ABC']),  # start of sentence.
            self.TestData(text='blah.ABC blah.')  # invalid start of sentence.
        )

    def test_unkown__end_boundaries(self):
        self.assert_abbreviations(
            self.TestData(text='blah blah ABC', unknown=['ABC']),  # end of sentence: 0 punct.
            self.TestData(text='blah blah ABC.', unknown=['ABC.']),  # end of sentence: 1 punct.
            self.TestData(text='blah blah ABC..', unknown=['ABC.']),  # end of sentence: 2+ puncts.
            self.TestData(text='blah ABC. Blah', unknown=['ABC']),  # end + new sentence.
            self.TestData(text='blah ABC.Blah'),  # end + invalid new sentence.
            self.TestData(text='blah ABC. blah', unknown=['ABC.']),  # middle of sentence.
            self.TestData(text='blah ABC.blah')  # invalid in middle of sentence.
        )

    def test_unknown__mixed_casing(self):
        self.assert_abbreviations(
            self.TestData(text='ABC blah blah', unknown=['ABC']),  # all caps.
            self.TestData(text='AbC blah blah', unknown=['AbC']),  # start and end caps.
            self.TestData(text='aBC blah blah'),  # end caps.
            self.TestData(text='ABc blah blah'),  # start caps.
            self.TestData(text='abc blah blah')  # no caps.
        )

    def test_unknown__mixed_periods(self):
        self.assert_abbreviations(
            self.TestData(text='blah A.B.C. blah', unknown=['A.B.C.']),
            self.TestData(text='blah AB.C. blah', unknown=['AB.C.']),
            self.TestData(text='blah A.BC. blah', unknown=['A.BC.']),
            self.TestData(text='blah A.B.C blah', unknown=['A.B.C']),
            self.TestData(text='blah ABC. blah', unknown=['ABC.']),
            self.TestData(text='blah AB.C blah', unknown=['AB.C']),
            self.TestData(text='blah A.BC blah', unknown=['A.BC']),
            self.TestData(text='blah ABC blah', unknown=['ABC'])
        )
