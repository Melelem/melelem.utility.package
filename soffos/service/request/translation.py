from ._base import ServiceRequestSession
from typing import List

class TranslationService(ServiceRequestSession):
    name = "soffos-service-translation"

    def translate(
        self,
        texts: List[str],
        target_language_code: str = None,
        source_language_code: str = None,
        auto_detect: bool = None
    ):

        json = {"texts": texts}
        if target_language_code:
            json["target_language_code"] = target_language_code
        if source_language_code:
            json["source_language_code"] = source_language_code
        if auto_detect:
            json["auto_detect"] = auto_detect

        return self.request(json=json)

    def detect(self, texts: List[str]):
        return self.request(json={"texts": texts}, path="detect")
