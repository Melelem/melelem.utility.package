from unittest import TestCase

from soffos.pre_processing.text import (
    TextSpan,
    remove_possessions,
    split_punctuations,
    normalize_chars,
    normalize_whitespaces
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

    def test_split(self):
        text = 'The dog is derived from an ancient, extinct wolf.'
        text_spans = TextSpan.split(text, spans=[(24, 26), (0, 3)])
        self.assertListEqual(text_spans, [
            TextSpan(text=' dog is derived from ', span=(3, 24)),
            TextSpan(text=' ancient, extinct wolf.', span=(26, len(text)))
        ])


class Tests(TestCase):
    def test_remove_possessions(self):
        text = remove_possessions('Mary\'s dog.')
        self.assertEqual(text, 'Mary dog.')

        text = remove_possessions('Mary\'s')
        self.assertEqual(text, 'Mary')

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
