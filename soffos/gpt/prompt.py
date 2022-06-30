from .gpt_utils import calculate_token_count_from_chars


class Prompt:
    """
    Manages the prompt used by AI routines
    """
    _prompt = None
    _prompt_token_count = 0

    def __init__(self, prompt_path :str):
        if self._prompt is not None:
            return
        with open( prompt_path, 'r', encoding='utf-8') as prompt_file:
            self._prompt = prompt_file.read()
        self._prompt_token_count = calculate_token_count_from_chars(self.char_count)

    @property
    def text(self):
        """
        Simple getter. Returns the prompt itself
        """
        return self._prompt

    @property
    def char_count(self):
        """
        Simple getter. Returns the prompt char length
        """
        if self._prompt is not None:
            return len(self._prompt)
        return 0

    @property
    def word_count(self):
        """
        Simple getter. Returns the num. of words in prompt
        """
        if self._prompt is not None:
            return len(self._prompt.split())
        return 0

    @property
    def token_count(self):
        """
        Simple getter. Returns the prompt's token count
        """
        return self._prompt_token_count
