"""
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2022-04-30
Purpose: General web client
"""

import json
import typing as t

import requests
from urllib3.util.retry import Retry

Payload = t.NewType('Payload', t.Dict[str, t.Any])


class WebClient:
    """
    General class for web requests
    """

    method: str = 'POST'
    url: str
    timeout: float = 600.0

    class Error(Exception):
        """General WebClient error"""

    def __init__(self, payload: t.Optional[Payload], url: t.Optional[str] = None):
        """
        Parameters
        ----------

        - payload(optional): used to send information to the server
        - url(optional): if provided, builds a client capable to send requests
          to provided url.
        """
        if self.method in ['POST', 'PUT', 'PATCH'] and payload is None:
            raise self.Error(
                f'{self.method} requests must always provide a payload')

        self.payload = payload
        if url is not None:
            self.url = url

    def send(self) -> t.Optional[Payload]:
        """
        Sends a request, collecting its results.

        Note
        ----
        If request cannot be done, fails and raise an Error exception
        """
        # pylint: disable=broad-except
        try:
            response: requests.Response = self.call_remote_endpoint()
            if not response.ok:
                try:
                    response_json = response.json()
                except requests.exceptions.JSONDecodeError:
                    response_json = None
                raise Exception(json.dumps({
                    'status_code': response.status_code,
                    'json': response_json
                }))
        except Exception as excpt:
            raise self.Error from excpt

    def call_remote_endpoint(self) -> t.Optional[requests.Response]:
        """
        Executes the request accordingly.

        Do not call this method directly. This is a customization point so one
        can customize how a request is sent to the target url.
        """
        return requests.request(
            method=self.method,
            url=self.url,
            json=self.payload,
            timeout=self.timeout
        )


class RetryWebClient(WebClient):
    """
    Web client capable of executing retries
    """

    retry_total: int = 3
    retry_backoff_factor: float = 0.1
    retry_status_forcelist: t.Set[int] = {429}
    session_mounts: t.Set[str] = {'http://', 'https://'}
    default_backoff_max: int = 3600

    def __init__(self, payload: t.Optional[Payload], url: t.Optional[str] = None):
        super().__init__(payload, url)

        Retry.DEFAULT_BACKOFF_MAX = self.default_backoff_max
        retry = Retry(
            total=self.retry_total,
            backoff_factor=self.retry_backoff_factor,
            status_forcelist=self.retry_status_forcelist
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session = requests.Session()
        for prefix in self.session_mounts:
            session.mount(prefix, adapter)
        self.session = session

    def call_remote_endpoint(self) -> t.Optional[requests.Response]:
        return self.session.request(
            self.method,
            self.url,
            timeout=self.timeout,
            json=self.payload
        )
