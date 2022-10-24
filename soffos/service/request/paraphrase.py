from ._base import ServiceRequestSession
from typing import List


class ParaphraseService(ServiceRequestSession):
    name = "soffos-service-paraphrase"

    def paraphrase(
        self,
        text: str,
        engine: str,
        llm_api_key: str = None,
        simplify: bool = None,
        sentence_split : int = None
    ):

        json = {
            "text": text,
            "engine": engine
        }
        
        if llm_api_key is not None:
            json['llm_api_key'] = llm_api_key
        if simplify is not None:
            json["simplify"] = simplify
        if sentence_split is not None:
            json["sentence_split"] = sentence_split
        
        return self.request(json=json)

    def reload_paraphrase_prompt(self, filename: str = None):

        json = {}
        if filename is not None:
            json["filename"] = filename

        return self.request(json={"filename": filename}, path="prompt/paraphrase/reload")
    
    def reload_simplify_prompt(self, filename: str = None):

        json = {}
        if filename is not None:
            json["filename"] = filename

        return self.request(json={"filename": filename}, path="prompt/simplify/reload")
