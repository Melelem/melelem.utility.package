from __future__ import annotations
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
        max_func: t.Callable[[Chunk], bool] = None,
        sentence_overlap: int = 0
    ):
        """Split text into collections of sentences (chunks). Chunk sizes may be limited by their
        number of characters, sentences, words. To disable a max limitation, set its value to 0. At
        least one max limit must be set. Sentences between chunks may also be overlapped.

        :param text: Text to be split into chunks.
        :param max_words: Max number of words a chunk may contain, defaults to 0.
        :param max_sentences: Max number of sentences a chunk may contain, defaults to 0.
        :param max_characters: Max number of characters a chunk may contain, defaults to 0.
        :param max_func: Callable which returns true on custom max condition, defaults to None.
        :param sentence_overlap: The number of sentences to overlap between chunks, defaults to 0.
        :return: A list of chunks.
        """
        if not max_func and all(max_value < 1 for max_value in [
            max_words, max_sentences, max_characters
        ]):
            raise ValueError(
                'At least one of the max arguments must be >= 1 or provide a max function.'
            )

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
            ) or (
                max_func and max_func(cls(sentences=[sentence]))
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
                ) or (
                    max_func and max_func(cls(sentences=chunk + [next_sentence]))
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


def remove_overlaps(chunks: t.List[t.Union[dict, Chunk]]) -> str:
    """
    This function is useful when pulling chunks from Elasticsearch and we want to 
    remove the overlaps so that the text is concatenated and passed to services such as GPT-3
    as one passage.

    Args:
        chunks (t.List[t.Union[dict, Chunk]]): List of dictionaries as they are retrieved from Elasticsearch, or Chunk objects.

    Returns:
        str: Joined de-overlapped text.
    """
    if isinstance(chunks[0], dict):
        content_key = 'content' if 'content' in chunks[0] else 'text'
        if 'meta' in chunks:
            chunks = sorted(chunks, key=lambda x: x['meta']['chunk_id'], reverse=True)
        text = ' '.join([c[content_key] for c in chunks])
    else:
        text = ' '.join(c.text for c in chunks)

    sents = [s.text for s in Sentence.from_text(text)]
    unique_sents = []
    for s in sents:
        if s not in unique_sents:
            unique_sents.append(s)

    return ' '.join(unique_sents)
