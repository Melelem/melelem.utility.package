import typing as t
from urllib3.util.retry import Retry
from json import dumps as json_dumps

import requests
import os

from ...settings import get_service_url, DEBUG
from ..exceptions import BadRequestException, InternalServerErrorException


Response = t.TypeVar('Response')


class ServiceRequestSession:

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
        response_type: t.Type[Response] = None
    ) -> Response: ...

    def request(
        self,
        json: t.Dict[str, t.Any],
        path: str = None,
        timeout: float = None,
        headers: t.Dict[str, str] = None,
        response_type: t.Type[Response] = None
    ):
        try:
            # Build request.
            if DEBUG:
                try:
                    authorization = os.environ['SOFFOS_API_KEY']
                    if headers is not None:
                        headers['Authorization'] = authorization
                    else:
                        headers = {"Authorization": authorization}
                except KeyError as ex:
                    raise Exception("Please specify a Soffos API key in the environment variable SOFFOS_API_KEY") from ex
                    
                url = 'https://dev-api.soffos.ai/service/service/'
                json = {
                    'name': self.name,
                    'request': json
                }
                if path:
                    json['path'] = path
                if response_type in [bytes, str]:
                    json['response_type'] = response_type.__name__
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
                if response.status_code == 400:
                    raise BadRequestException(**response.json())
                else:
                    raise InternalServerErrorException(
                        service=self.name,
                        message='Service error',
                        details=response.json()
                    )

            # Unpack response.
            response_json: t.Dict[str, t.Any]
            if DEBUG:
                # Handle response type.
                response_json = response.json()['response']
                if response_type == bytes:
                    # NOTE: Treat with caution! Should only run locally for security!
                    return eval(response_json)
                elif response_type == str:
                    return json_dumps(response_json)
            else:
                # Handle response type.
                if response_type == bytes:
                    return response.content
                elif response_type == str:
                    return response.text
                else:
                    response_json = response.json()

            # Optional: create response object.
            return response_type(**response_json) if response_type else response_json

        # Cast unknown errors.
        except Exception as ex:
            raise ex
