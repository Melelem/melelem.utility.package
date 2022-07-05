from ..service import Service
from .prompt import Prompt
from .gpt_utils import *
from ..web import Payload
import typing as t
import re


class GPTService(Service):
    """
    Service template for using gpt3 with specific prompt
    TODO: Describe this class better
    """
    def validate(self, request_data):
        if (not request_data["text"]) :
            raise TypeError('The input text is missing')
            
        if (not request_data["max_tokens"]) :
            raise TypeError('max num of tokens not specified')
            
        if (not request_data["engine"]) or (request_data["engine"] not in ['text-davinci-002','text-curie-001','text-babbage-001','text-ada-001']):
            raise TypeError('engine is missing or does not exist')

        max_char_count = calculate_chars_count_from_tokens(4000) if request_data["engine"] == 'text-davinci-002' else calculate_chars_count_from_tokens(2048)
        completion_char_count = calculate_chars_count_from_tokens(request_data["max_tokens"])
        text_char_count = len(request_data["text"])    

        prompt=self.load_prompt(request_data)

        if prompt.char_count + text_char_count + completion_char_count > max_char_count:
            raise ValueError(f'The combined length of prompt, provided text and provided max_tokens should not exceed {max_char_count} characters for the engine: {request_data["engine"]}. Prompt length: ~{prompt.char_count}, provided text: ~{text_char_count}, provided max_tokens: {request_data["max_tokens"]} = ~{completion_char_count} characters.')
   
    def craft_prompt(self, text: str ,prompt:Prompt,end_str:str):
        return prompt.text + text + end_str

    def process_predictions(self, predictions: str, compile_pattern:str):
        pattern = re.compile(compile_pattern)
        result = pattern.findall(predictions)
        return result    

    def load_prompt(self,request_data):
        raise NotImplementedError()

    def price_calculations(self):
        pass 

