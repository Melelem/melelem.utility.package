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
    def from_text(
        cls,
        text: str,
        max_words: int = 0,
        max_sentences: int = 0,
        max_characters: int = 0,
        sentence_overlap: int = 0
    ):
        """Split text into collections of sentences (chunks). Chunk sizes may be limited by their
        number of characters, sentences, words. To disable a max limitation, set its value to 0. At
        least one max limit must be set. Sentences between chunks may also be overlapped.

        :param text: Text to be split into chunks.
        :param max_words: Max number of words a chunk may contain, defaults to 0.
        :param max_sentences: Max number of sentences a chunk may contain, defaults to 0.
        :param max_characters: Max number of characters a chunk may contain, defaults to 0.
        :param sentence_overlap: The number of sentences to overlap between chunks, defaults to 0.
        :return: A list of chunks.
        """
        if all(max_value < 1 for max_value in [max_words, max_sentences, max_characters]):
            raise ValueError('At least one of the max arguments must be >= 1.')

        sentences = Sentence.from_text(text)
        sentence_count = len(sentences)
        sentence_index = 0

        chunks: t.List[cls] = []
        while sentence_index < sentence_count:
            # Get sentence and validate its length.
            sentence = sentences[sentence_index]
            if (
                max_characters and sentence.length > max_characters
            ) or (
                max_words and len(sentence.words) > max_words
            ):
                sentence_index += 1
                continue

            # Add next sentences to chunk until its size limits are exceeded.
            chunk = [sentence]
            for next_sentence in sentences[sentence_index + 1:]:
                if (
                    max_sentences and len(chunk) + 1 > max_sentences
                ) or (
                    max_characters
                    and sum(s.length for s in chunk + [next_sentence]) > max_characters
                ) or (
                    max_words
                    and sum(len(s.words) for s in chunk + [next_sentence]) > max_words
                ):
                    break
                chunk.append(next_sentence)

            # Increase index by chunk size and decrease by max sentence overlap length.
            chunk_sentence_count = len(chunk)
            sentence_index += chunk_sentence_count
            # NOTE: Can't overlap a single sentence and the last sentence.
            if chunk_sentence_count > 1 and sentence_index < sentence_count:
                sentence_index -= (
                    sentence_overlap
                    if sentence_overlap < chunk_sentence_count
                    else chunk_sentence_count - 1
                )

            chunks.append(cls(sentences=chunk))

        return chunks
