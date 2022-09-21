from ._base import ServiceRequestSession


class QueryParserService(ServiceRequestSession):
    name = "soffos-service-query-parser"

    def parse(
        self, 
        query: str,
        profanities: bool = None,
        short: bool = None,
        invalid_language: bool = None,
        intents: bool = None,
        ambiguous_pronouns: bool = None,
        classification: bool = None
    ):

        json = {"query": query}
        
        if profanities is not None:
            json["profanities"] = profanities
        if short is not None:
            json["short"] = short
        if invalid_language is not None:
            json["invalid_language"] = invalid_language
        if intents is not None:
            json["intents"] = intents
        if ambiguous_pronouns is not None:
            json["ambiguous_pronouns"] = ambiguous_pronouns
        if classification is not None:
            json["classification"] = classification

        return self.request(json=json)
