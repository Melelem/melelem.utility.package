
from ...settings import get_service_url, DEBUG
from ...web import RetryWebClient


class ServiceRequestSession(RetryWebClient):
    name: str
    path = ''

    def __init__(self, payload):
        if DEBUG:
            payload = {
                'name': self.name,
                'request': payload
            }
            if self.path:
                payload['path'] = self.path
            url = 'https://dev-api.soffos.ai/service/'
        else:
            url = get_service_url(self.name) + self.path
        super().__init__(payload, url)

    def send(self):
        response = super().send()
        if DEBUG:
            response = response['response']
        return response
