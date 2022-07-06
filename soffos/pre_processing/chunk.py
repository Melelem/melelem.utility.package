import typing as t
from dataclasses import dataclass

from .sentence import Sentence


@dataclass(frozen=True)
class Chunk:
    """A chunk is a collection of sentences."""
    sentences: t.List[Sentence]

    @property
    def text(self):
        return ' '.join(sentence.text for sentence in self.sentences)

    @property
    def span_start(self):
        return self.sentences[0].span_start

    @property
    def span_end(self):
        return self.sentences[-1].span_end

    @property
    def span(self):
        return self.span_start, self.span_end

    @classmethod
    def from_text(cls, text: str, max_chars: int, sentence_overlap: int = 0):
        sentences = Sentence.from_text(text)
        sentence_count = len(sentences)
        sentence_index = 0

        chunks: t.List[cls] = []
        while sentence_index < sentence_count:
            # Chunk is initialized with first sentence.
            sentence = sentences[sentence_index]
            chunk_sentences = [sentence]

            # Add as many next sentences to chunk until chunk exceeds max word limit.
            if sentence.length < max_chars:
                for next_sentence in sentences[sentence_index + 1:]:
                    # Add next sentence if new word length does not exceed limit.
                    if sum(s.length for s in chunk_sentences + [next_sentence]) > max_chars:
                        break
                    chunk_sentences.append(next_sentence)

            # Increase index by sentence length of chunk and decrease by max sentence overlap length.
            chunk_sentences_count = len(chunk_sentences)
            sentence_index += chunk_sentences_count
            # NOTE: Can't overlap a single sentence and the last sentence.
            if chunk_sentences_count > 1 and sentence_index < sentence_count:
                sentence_index -= (
                    sentence_overlap
                    if sentence_overlap < chunk_sentences_count
                    else chunk_sentences_count - 1
                )

            chunks.append(cls(sentences=chunk_sentences))

        return chunks
