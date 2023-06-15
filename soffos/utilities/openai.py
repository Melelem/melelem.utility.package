from enum import Enum
import tiktoken
import typing as t
from itertools import chain

class Tokenizer:
    def __init__(self) -> None:
        self.tokenizers = {}
    def __call__(self, engine):
        if engine not in self.tokenizers:
            self.tokenizers[engine] = tiktoken.encoding_for_model(engine)
        return self.tokenizers[engine]

TOKENIZER = Tokenizer()

class GPTEngine(str, Enum):
    gpt4_8k = 'gpt-4'
    gpt4_32k = 'gpt-4-32k' 
    chatgpt = 'gpt-3.5-turbo'
    chatgpt_0613 = 'gpt-3.5-turbo-0613'
    chatgpt_0613_16k = 'gpt-3.5-turbo-16k-0613'
    davinci = 'text-davinci-003'
    curie = 'text-curie-001'
    babbage = 'text-babbage-001'
    ada = 'text-ada-001'
    ada_embedding = 'text-embedding-ada-002'

class GPTEngineSpecifications(t.NamedTuple):
    max_tokens: int

GPT_ENGINE_SPECS = {
    GPTEngine.gpt4_8k: GPTEngineSpecifications(
        max_tokens=8192
    ),
    GPTEngine.gpt4_32k: GPTEngineSpecifications(
        max_tokens=32768
    ),
    GPTEngine.chatgpt: GPTEngineSpecifications(
        max_tokens=4096
    ),
    GPTEngine.chatgpt_0613: GPTEngineSpecifications(
        max_tokens=4096
    ),
    GPTEngine.chatgpt_0613_16k: GPTEngineSpecifications(
        max_tokens=16384
    ),
    GPTEngine.davinci: GPTEngineSpecifications(
        max_tokens=4000
    ),
    GPTEngine.curie: GPTEngineSpecifications(
        max_tokens=2048
    ),
    GPTEngine.babbage: GPTEngineSpecifications(
        max_tokens=2048
    ),
    GPTEngine.ada: GPTEngineSpecifications(
        max_tokens=2048
    ),
    GPTEngine.ada_embedding: GPTEngineSpecifications(
        max_tokens=8192
    )
}

class Prompt:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as prompt_file:
            self.text = prompt_file.read()
        self.char_count = len(self.text)
        self.word_count = len(self.text.split())
    
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
                raise ValueError(f"The literal string to be replaced \"{literal}\" is not following the required convention. \
                                 Please provide a string enclosed with curlies and double underscores, for example: \"{example}\"")
            text = text.replace(literal, replacement)

        return text
    
Usage = t.Dict[str, t.Any]

def calculate_usage_overview(usages: t.List[Usage]):

    keys = list(set(chain.from_iterable(u.keys() for u in usages)))
    
    return {
        'calls': len(usages),
        **{k: sum([u.get(k, 0) for u in usages]) for k in keys}
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

    return GPT_ENGINE_SPECS[engine].max_tokens - len(TOKENIZER(engine.value).encode(prompt))

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens