from enum import Enum
import tiktoken
import typing as t
import re

GPT3_TOKENIZER = tiktoken.get_encoding("gpt2")

class GPTEngine(str, Enum):
    chat = 'gpt-3.5-turbo'
    davinci = 'text-davinci-003'
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
        self.token_count = len(GPT3_TOKENIZER.encode(self.text)) if self.text else 0
    
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
    GPTEngine.chat: GPTEngineSpecifications(
        price_per_1k_tokens=0.002,
        max_tokens=4096
    ),
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


def calculate_max_allowed_tokens(
    engine: GPTEngine,
    prompt: str
):
    """Calculates how many tokens are remaining for completion given the model size and prompt.

    Args:
        engine (GPTEngine): The engine.
        prompt (str): The prompt.
    """

    return GPT_ENGINE_SPECS[engine].max_tokens - len(GPT3_TOKENIZER.encode(prompt))

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")