import math

MODEL_GPT_TOKEN_CHAR_COUNT=4

def calculate_token_count_from_chars(data_length: int) -> int:
    """
    Calculates the token count from a given data. This method is based
    in english language tokens.
    Parameters
    ----------
    - data_length: Data length in character means
    Returns
    -------
    - Calculated token count
    """
    return math.ceil(data_length / MODEL_GPT_TOKEN_CHAR_COUNT)


def calculate_chars_count_from_tokens(data_length: int) -> int:
    """
    Calculates the char count from a given data. This method is based
    in english language tokens.
    Parameters
    ----------
    - data_length: Data length in tokens
    Returns
    -------
    - Calculated chars count
    """
    return data_length * MODEL_GPT_TOKEN_CHAR_COUNT    