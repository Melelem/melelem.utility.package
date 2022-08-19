from ._base import ServiceRequestSession
from typing import List


class ParaphraseService(ServiceRequestSession):
    name = "soffos-service-paraphrase"

    def paraphrase(
        self,
        text: str,
        engine: str,
        max_tokens: int = None,
        simplify: bool = None,
        sentence_split : int = None
    ):

        json = {
            "text": text,
            "engine": engine
        }

        if max_tokens:
            json["max_tokens"] = max_tokens
        if simplify:
            json["simplify"] = simplify
        if sentence_split:
            json["sentence_split"] = sentence_split
        
        return self.request(json=json)

    def reload_paraphrase_prompt(self, filename: str = None):

        json = {}
        if filename:
            json["filename"] = filename

        return self.request(json={"filename": filename}, path="prompt/paraphrase/reload")
    
    def reload_simplify_prompt(self, filename: str = None):

        json = {}
        if filename:
            json["filename"] = filename

        return self.request(json={"filename": filename}, path="prompt/simplify/reload")
