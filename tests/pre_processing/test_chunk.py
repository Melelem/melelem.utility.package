from unittest import TestCase

from soffos.pre_processing import Sentence
from soffos.pre_processing.chunk import Chunk


class ChunkTests(TestCase):
    def test_from_text(self):
        text = 'One. Two. Three. Four. Five.'
        chunks = Chunk.from_text(text, max_chars=10)
        self.assertListEqual(chunks, [
            Chunk(sentences=[
                Sentence(text='One.', span=(0, 4)),
                Sentence(text='Two.', span=(5, 9))
            ]),
            Chunk(sentences=[
                Sentence(text='Three.', span=(10, 16)),
            ]),
            Chunk(sentences=[
                Sentence(text='Four.', span=(17, 22)),
                Sentence(text='Five.', span=(23, 28))
            ])
        ])

    def test_from_text__sentence_overlap_1(self):
        text = 'One. Two. Three. Four. Five.'
        chunks = Chunk.from_text(text, max_chars=10, sentence_overlap=1)
        self.assertListEqual(chunks, [
            Chunk(sentences=[
                Sentence(text='One.', span=(0, 4)),
                Sentence(text='Two.', span=(5, 9))
            ]),
            Chunk(sentences=[
                Sentence(text='Two.', span=(5, 9)),
                Sentence(text='Three.', span=(10, 16)),
            ]),
            Chunk(sentences=[
                Sentence(text='Three.', span=(10, 16))
            ]),
            Chunk(sentences=[
                Sentence(text='Four.', span=(17, 22)),
                Sentence(text='Five.', span=(23, 28))
            ])
        ])
