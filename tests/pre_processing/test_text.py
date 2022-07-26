from unittest import TestCase

from soffos.pre_processing.text import (
    TextSpan,
    remove_possessions,
    normalize_chars
)


class TextSpanTests(TestCase):
    def test_words(self):
        text = ' Hi. Hello, how     are you? I like them - apples!!'
        words = TextSpan(text=text, span=(0, len(text))).words
        self.assertListEqual(words, [
            'Hi', 'Hello', 'how', 'are', 'you', 'I', 'like', 'them', 'apples'
        ])

    def test_words__one_word(self):
        text = ' Hello.   '
        words = TextSpan(text=text, span=(0, len(text))).words
        self.assertListEqual(words, ['Hello'])

    def test_words__no_words(self):
        text = '    '
        words = TextSpan(text=text, span=(0, len(text))).words
        self.assertListEqual(words, [])

    def test_merge_spans(self):
        spans = [
            (0, 5),
            (15, 20),
            (4, 10),
            (20, 25),
            (26, 30),
            (9, 12)
        ]
        merged_spans = TextSpan.merge_spans(spans)
        self.assertListEqual(merged_spans, [
            (0, 12),
            (15, 25),
            (26, 30)
        ])

    def test_split(self):
        text = 'The dog is derived from an ancient, extinct wolf.'
        text_spans = TextSpan.split(text, spans=[(24, 26), (1, 3), (0, 2)])
        self.assertListEqual(text_spans, [
            TextSpan(text=' dog is derived from ', span=(3, 24)),
            TextSpan(text=' ancient, extinct wolf.', span=(26, len(text)))
        ])

    def test_get_non_overlapping_spans(self):
        spans, other_spans = [(0, 5), (6, 10)], [(8, 12), (10, 15)]
        non_overlapping_spans = TextSpan.get_non_overlapping_spans(spans, other_spans)
        self.assertListEqual(non_overlapping_spans, [
            (10, 15)
        ])


class Tests(TestCase):
    def test_remove_possessions(self):
        text = remove_possessions('Mary\'s dog.')
        self.assertEqual(text, 'Mary dog.')

        text = remove_possessions('Mary\'s')
        self.assertEqual(text, 'Mary')

    def test_normalize_chars(self):
        characters = {
            '“': '"',
            '”': '"',
            '‘': '\'',
            '’': '\'',
            '\'\'': '"',
            '``': '"',
            '–': '-'
        }
        text = ', '.join(characters.keys())
        normalized_text = normalize_chars(text)
        expected_normalized_text = ', '.join(characters.values())
        self.assertEqual(normalized_text, expected_normalized_text)
