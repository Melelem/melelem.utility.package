from unittest import TestCase

from soffos.pre_processing import TextSpan
from soffos.pre_processing.profanity import get_profanities


class Tests(TestCase):
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
