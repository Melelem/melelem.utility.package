import typing as t
from urllib3.util.retry import Retry
from json import dumps as json_dumps

import requests

from ...settings import get_service_url, DEBUG


Response = t.TypeVar('Response')


class ServiceRequestSession:

    class Error(Exception):
        pass

    name: str

    def __init__(
        self,
        retry_total: int = 3,
        retry_backoff_factor: float = 0.1,
        retry_status_forcelist: t.Set[int] = {429}
    ):
        self._session = requests.Session()

        http_adapter = requests.adapters.HTTPAdapter(max_retries=Retry(
            total=retry_total,
            backoff_factor=retry_backoff_factor,
            status_forcelist=retry_status_forcelist
        ))
        for prefix in {'http://', 'https://'}:
            self._session.mount(prefix, http_adapter)

    @t.overload
    def request(
        self,
        json: t.Dict[str, t.Any],
        path: str = None,
        timeout: float = None,
        headers: t.Dict[str, str] = None
    ) -> t.Dict[str, t.Any]: ...

    @t.overload
    def request(
        self,
        json: t.Dict[str, t.Any],
        path: str = None,
        timeout: float = None,
        headers: t.Dict[str, str] = None,
        response_cls: t.Type[Response] = None
    ) -> Response: ...

    def request(
        self,
        json: t.Dict[str, t.Any],
        path: str = None,
        timeout: float = None,
        headers: t.Dict[str, str] = None,
        response_cls: t.Type[Response] = None
    ):
        try:
            # Build request.
            if DEBUG:
                url = 'https://dev-api.soffos.ai/api/service/'
                json = {
                    'name': self.name,
                    'request': json
                }
                if path:
                    json['path'] = path
            else:
                url = get_service_url(self.name)
                if path:
                    url += path

            # Send request and get response.
            response = self._session.request(
                method='POST',
                url=url,
                timeout=timeout,
                json=json,
                headers=headers
            )

            # Validate response is ok.
            if not response.ok:
                error = {'status_code': response.status_code}
                try:
                    error['json'] = response.json()
                except requests.exceptions.JSONDecodeError:
                    pass
                raise self.Error(json_dumps(error))

            # Get response json.
            response_json: t.Dict[str, t.Any] = response.json()
            response_json = response_json['response'] if DEBUG else response_json

            # Optional: create response object.
            return response_cls(**response_json) if response_cls else response_json

        # Re-raise known errors.
        except self.Error as ex:
            raise ex
        # Cast unknown errors.
        except Exception as ex:
            raise self.Error from ex
