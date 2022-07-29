import typing as t
from enum import Enum


class Engine(str, Enum):
    davinci = 'text-davinci-002'
    curie = 'text-curie-001'
    babbage = 'text-babbage-001'
    ada = 'text-ada-001'


class EngineSpecifications(t.NamedTuple):
    price_per_1k_tokens: float
    max_tokens: int


ENGINE_SPECS = {
    Engine.davinci: EngineSpecifications(
        price_per_1k_tokens=0.06,
        max_tokens=4000
    ),
    Engine.curie: EngineSpecifications(
        price_per_1k_tokens=0.006,
        max_tokens=2048
    ),
    Engine.babbage: EngineSpecifications(
        price_per_1k_tokens=0.0012,
        max_tokens=2048
    ),
    Engine.ada: EngineSpecifications(
        price_per_1k_tokens=0.0008,
        max_tokens=2048
    )
}


def calculate_remaining_prompt_length(
    engine: Engine,
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
        (ENGINE_SPECS[engine].max_tokens * 4)
        - prompt_length
        - (completion_max_tokens * 4)
    )
