from unittest import TestCase

from soffos.pre_processing.text import (
    load_stopwords,
    TextSpan,
    split_punctuations,
    split_stopwords,
    get_profanities
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
