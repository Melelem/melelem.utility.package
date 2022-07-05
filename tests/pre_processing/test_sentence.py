from unittest import TestCase

from soffos.pre_processing.sentence import Sentence


class SentenceTests(TestCase):
    def test_from_text(self):
        sentence_texts = [
            'The dog or domestic dog (Canis familiaris[4][5] or Canis lupus familiaris[5]) is a domesticated descendant of the wolf, and is characterized by an upturning tail.',
            'The dog is derived from an ancient, extinct wolf,[6][7] and the modern wolf is the dog\'s nearest living relative.',
            'The dog was the first species to be domesticated, [9][8] by hunter-gatherers over 15, 000 years ago, [7] before the development of agriculture.',
            'Due to their long association with humans, dogs have expanded to a large number of domestic individuals[10] and gained the ability to thrive on a starch-rich diet that would be inadequate for other canids.',
            'The dog has been selectively bred over millennia for various behaviors, sensory capabilities, and physical attributes.',
            'Dog breeds vary widely in shape, size, and color.',
            'They perform many roles for humans, such as hunting, herding, pulling loads, protection, assisting police and the military, companionship, therapy, and aiding disabled people.',
            'Over the millennia, dogs became uniquely adapted to human behavior, and the human-canine bond has been a topic of frequent study.',
            'This influence on human society has given them the sobriquet of "man\'s best friend".'
        ]
        text = ' '.join(sentence_texts)
        sentences = Sentence.from_text(text)
        expected_sentences = []
        for sentence_text in sentence_texts:
            index = text.index(sentence_text)
            expected_sentences.append(Sentence(
                text=sentence_text,
                span=(index, index + len(sentence_text))
            ))
        self.assertListEqual(sentences, expected_sentences)

    def test_from_text__abbreviations(self):
        text = 'Hello Dr. Susan! Have you read about the new A.B.C. research?'
        sentences = Sentence.from_text(text)
        self.assertListEqual(sentences, [
            Sentence(text='Hello Dr. Susan!', span=(0, 16)),
            Sentence(text='Have you read about the new A.B.C. research?', span=(17, 61))
        ])

    def test_from_text__urls(self):
        text = 'Want to learn about NLP? Visit https://www.soffos.ai/ for info.'
        sentences = Sentence.from_text(text)
        self.assertListEqual(sentences, [
            Sentence(text='Want to learn about NLP?', span=(0, 24)),
            Sentence(text='Visit https://www.soffos.ai/ for info.', span=(25, 63))
        ])
