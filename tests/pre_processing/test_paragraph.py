from unittest import TestCase

from soffos.pre_processing.paragraph import Paragraph


class ParagraphTests(TestCase):
    def test_from_text(self):
        paragraphs = Paragraph.from_text('''
ab.
c

d!!!!


...e
''')
        self.assertListEqual(paragraphs, [
            Paragraph(text='ab.', span=(1, 4)),
            Paragraph(text='c', span=(5, 6)),
            Paragraph(text='d!!!!', span=(8, 13)),
            Paragraph(text='...e', span=(16, 20))
        ])
