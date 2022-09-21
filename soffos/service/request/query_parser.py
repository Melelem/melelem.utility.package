from ._base import ServiceRequestSession


class QueryParserService(ServiceRequestSession):
    name = "soffos-service-query-parser"

    def parse(self, message: str):
        return self.request(json={"message": message})
