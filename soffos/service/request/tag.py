import typing as t

from ._base import ServiceRequestSession


class TagService(ServiceRequestSession):
    name = 'soffos-service-tag'

    def generate_tags(
        self,
        texts: t.List[str],
        language: str = None,
        options_one_word: bool = None,
        options_two_words: bool = None,
        options_three_words: bool = None,
    ):
        json = {'texts': texts, 'options': {}}
        if language is not None:
            json['language'] = language
        if options_one_word is not None:
            json['options']['one_word'] = options_one_word
        if options_two_words is not None:
            json['options']['two_words'] = options_two_words
        if options_three_words is not None:
            json['options']['three_words'] = options_three_words
        return self.request(json)
