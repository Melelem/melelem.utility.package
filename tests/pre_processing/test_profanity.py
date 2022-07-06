from unittest import TestCase

from soffos.pre_processing.profanity import Profanity


class ProfanityTests(TestCase):
    def test_from_text__normal_casing(self):
        text_spans = Profanity.from_text('He is a bitch, she said.')
        self.assertListEqual(text_spans, [Profanity(text='bitch', span=(8, 13))])

    def test_from_text__mixed_casing(self):
        text_spans = Profanity.from_text('He is a BitCh, she said.')
        self.assertListEqual(text_spans, [Profanity(text='BitCh', span=(8, 13))])

    def test_from_text__char_substitution(self):
        text_spans = Profanity.from_text('He is a b!tCh, she said.')
        self.assertListEqual(text_spans, [Profanity(text='b!tCh', span=(8, 13))])

    def test_from_text__irregular_spacing(self):
        text_spans = Profanity.from_text('dry     hump')
        self.assertListEqual(text_spans, [Profanity(text='dry     hump', span=(0, 12))])

    def test_from_text__conjunction(self):
        # NOTE: 'ass' should not be matched
        text_spans = Profanity.from_text('asshole')
        self.assertListEqual(text_spans, [Profanity(text='asshole', span=(0, 7))])
