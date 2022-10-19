from ._base import ServiceRequestSession
import typing as t


class GPT3Service(ServiceRequestSession):
    name = 'soffos-service-gpt3'

    def generate(
        self,
        prompt: str,
        stop: str,
        max_tokens: int,
        engine: str = None,
        temperature: float = None,
        top_p: float = None,
        frequency_penalty: float = None,
        presence_penalty: float = None,
        logprobs: int = None,
        validate_prompt_content: bool = None,
        app: str = None,
        user: str = None
    ):
        """The generate endpoint calls the "Complete" engine of OpenAI.

        Args:
            prompt (str): Few-shot example prompt.
            stop (str): Stop sequence. Once this sequence of characters is generated, the model stops generating more text.
            max_tokens (int): Maximum allowed tokens to generate. Make sure this value added with the prompt length does not exceed the maxiumum input length of the model. Service default is 200.
            engine (str, optional): Which model to use. Defaults to None. Service default is "text-curie-001". Valid options: "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001".
            temperature (float, optional): The level of "creativity". Defaults to None. Service default is 0.0.
            top_p (float, optional): Controls diversity via nucleus sampling. 0.5 means half of all likelihood-weighted options are considered. Defaults to None. Service default is 1.0.
            frequency_penalty (float, optional): How much to penalize new tokens based on their frequency so far. Decreases the model's likelihood to repeat the same line verbatim. Defaults to None. Service default is 0.0.
            presence_penalty (float, optional): How much to penalize new tokens based on whether they appear in the text so far. Increases the model's likelihood to talk about new topics. Defaults to None. Service defailt is 0.0.
            validate_prompt_content (bool, optional): Whether to check if the content is sensitive or offensive. Defaults to None.

        Returns:
            _type_: OpenAIObject augmented with additional metadata such as costings.
        """

        json = {
            'prompt': prompt,
            'stop': stop,
            'max_tokens': max_tokens
        }

        if engine is not None:
            json["engine"] = engine
        if temperature is not None:
            json["temperature"] = temperature
        if top_p is not None:
            json["top_p"] = top_p
        if frequency_penalty is not None:
            json["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            json["presence_penalty"] = presence_penalty
        if logprobs is not None:
            json["logprobs"] = logprobs
        if validate_prompt_content is not None:
            json["validate_prompt_content"] = validate_prompt_content
        if app is not None:
            json['app'] = app
        if user is not None:
            json['user'] = user
        return self.request(json=json, path="generate")

    def count_tokens(self, text: str):
        return self.request(json={'text': text}, path='count-tokens')
