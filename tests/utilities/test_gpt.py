from unittest import TestCase

from soffos.utilities.gpt3 import (
    calculate_remaining_prompt_length,
    GPTEngine
)


class GptTests(TestCase):
    def test_calculate_remaining_prompt_length(self):
        remaining_prompt_length = calculate_remaining_prompt_length(
            GPTEngine.davinci,
            prompt_length=1000,
            completion_max_tokens=100
        )
        self.assertEqual(remaining_prompt_length, 14600)
