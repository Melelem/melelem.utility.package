import typing as t
from enum import Enum


class GPTEngine(str, Enum):
    davinci = 'text-davinci-002'
    curie = 'text-curie-001'
    babbage = 'text-babbage-001'
    ada = 'text-ada-001'


class GPTEngineSpecifications(t.NamedTuple):
    price_per_1k_tokens: float
    max_tokens: int


GPT_ENGINE_SPECS = {
    GPTEngine.davinci: GPTEngineSpecifications(
        price_per_1k_tokens=0.06,
        max_tokens=4000
    ),
    GPTEngine.curie: GPTEngineSpecifications(
        price_per_1k_tokens=0.006,
        max_tokens=2048
    ),
    GPTEngine.babbage: GPTEngineSpecifications(
        price_per_1k_tokens=0.0012,
        max_tokens=2048
    ),
    GPTEngine.ada: GPTEngineSpecifications(
        price_per_1k_tokens=0.0008,
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

def calculate_remaining_prompt_length(
    engine: GPTEngine,
    prompt_length: int,
    completion_max_tokens: int = 0
):
    """Calculate how many remaining characters are available in a prompt for a specific engine.

    :param engine: The engine called.
    :param prompt_length: The length of the base prompt.
    :param completion_max_tokens: The number of tokens allowed for text completion, defaults to 0.
    :return: The remaining number of characters you can include in the prompt for the engine.
    """
    return (
        (GPT_ENGINE_SPECS[engine].max_tokens * 4)
        - prompt_length
        - (completion_max_tokens * 4)
    )
