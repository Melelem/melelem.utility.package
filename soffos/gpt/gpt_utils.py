import math
import settings

MODEL_GPT_TOKEN_CHAR_COUNT=4

def calculate_token_count(data_length: int) -> int:
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