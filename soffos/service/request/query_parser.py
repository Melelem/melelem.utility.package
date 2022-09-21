from ._base import ServiceRequestSession


class QueryParserService(ServiceRequestSession):
    name = "soffos-service-query-parser"

    def parse(self, query: str):
        return self.request(json={"query": query})
