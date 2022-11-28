from ._base import ServiceRequestSession


class TransformerModelService(ServiceRequestSession):
    name = "soffos-service-model-transformers"

    def classify_queries(self, queries: list[str]):
        
        json = {"queries": queries}

        return self.request(json=json, path="classify-query")      

    def encode(self, texts: list[str], task: str = None):

        json = {"texts": texts}
        if task is not None:
            json["task"] = task
            
        return self.request(json=json, path="sentence-bert/encode")

    def extract_keywords(self, **kwargs):

        json = {**kwargs}

        return self.request(json=json, path="extract-keywords")

    def sentiment(self, texts: list[str]):

        json = {"texts": texts}

        return self.request(json=json, path="sentiment")
