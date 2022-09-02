from enum import Enum
import typing as t
import re


class GPTEngine(str, Enum):
    davinci = 'text-davinci-002'
    curie = 'text-curie-001'
    babbage = 'text-babbage-001'
    ada = 'text-ada-001'


class GPTEngineSpecifications(t.NamedTuple):
    price_per_1k_tokens: float
    max_tokens: int

class Prompt:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as prompt_file:
            self.text = prompt_file.read()
        self.char_count = len(self.text)
        self.word_count = len(self.text.split())
        self.token_count = self.chars_to_tokens(self.char_count)

    @classmethod
    def tokens_to_chars(self, tokens: int):
        return tokens*4
    
    @classmethod
    def chars_to_tokens(self, chars: int):
        return chars/4
    
    def format_text(self, replacements: t.Dict[str, str]):
        """
        Replaces the placeholders in the prompt with the required information.

        Args:
            replacements (t.Dict[str, str]): Dictionary with string literals to be replaced as keys
            and the replacement strings as values.

        Raises:
            ValueError: If the literal string is not following the convention.
            ValueError: If the literal string has been found more than once in the text.

        Returns:
            _type_: Propmpt's raw text with the replacements.
        """
        text = self.text
        for literal, replacement in replacements.items():
            if not literal.startswith("{__") or not literal.endswith("__}"):
                example = "{__replace__}"
                raise ValueError(f"The literal string to be replaced \"{literal}\" is not following the required convention. Please provide a string enclosed with curlies and double underscores, for example: \"{example}\"")
            if len([m for m in re.finditer(literal, text)]) > 1:
                raise ValueError(f"The literal string to be replaced \"{literal}\" has been found multiple times in the prompt. Please format the prompt with unique placeholders.")
            text = text.replace(literal, replacement)

        return text

GPT_ENGINE_SPECS = {
    GPTEngine.davinci: GPTEngineSpecifications(
        price_per_1k_tokens=0.02,
        max_tokens=4000
    ),
    GPTEngine.curie: GPTEngineSpecifications(
        price_per_1k_tokens=0.002,
        max_tokens=2048
    ),
    GPTEngine.babbage: GPTEngineSpecifications(
        price_per_1k_tokens=0.0005,
        max_tokens=2048
    ),
    GPTEngine.ada: GPTEngineSpecifications(
        price_per_1k_tokens=0.0004,
        max_tokens=2048
    )
}

Usage = t.Dict[str, t.Any]


def calculate_usage_overview(usages: t.List[Usage]):
    return {
        'prompt_tokens': sum(u['prompt_tokens'] for u in usages),
        'completion_tokens': sum(u['completion_tokens'] for u in usages),
        'total_tokens': sum(u['total_tokens'] for u in usages),
        'total_cost_dollars': sum(u['cost_dollars'] for u in usages),
        'calls': len(usages)
    }

#TODO: Implement an exact calculation using Transformer's GPT tokenizer and parametrize the option
# to either use a rough calculation (fast) or exact (slower).
def calculate_allowed_max_tokens(
        engine: GPTEngine, 
        prompt_len_chars: int,
        request_data_len_chars: int = 0
    ):
    """
    Calculate the maximum value that can be set for max_tokens when calling the GPT-3 service.
    This is the difference of the final formatted prompt's length from the maximum
    input length of the specific engine.
    This is not required for services that we expect a very small completion and where max_tokens
    can be set to a very low value.
    This is very useful for services with long completions. By using this function to calculate
    max_tokens, we effectively allow the model to generate up to the maximum number of tokens possible.
    The request_data_len_chars parameter is optional to allow the use of this function both in validators
    (where the prompt isn't yet formatted) and within the service itself where the prompt might be in its final form.

    Args:
        engine (GPTEngine): Engine being used.
        prompt_len_chars (int): Character length of the prompt.
        request_data_len_chars (int): Character length of anything that will be added to the prompt. When provided, the value for prompt_len_chars should be the length of the non-formatted prompt.
    """

    return Prompt.chars_to_tokens(
        chars=Prompt.tokens_to_chars(
            GPT_ENGINE_SPECS[engine].max_tokens
        ) - (prompt_len_chars + request_data_len_chars)
    )
