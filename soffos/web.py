"""
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2022-06-02
Purpose: Web related utilities
"""
import typing as t
from requests import request, Response
from requests.exceptions import RequestException

Payload = t.Dict[str, t.Any]


class CallbackWebhook:
    """
    Implements a web hook callback following Soffos standard protocol as
    described in this article:
    https://www.notion.so/soffos/Callback-Protocol-9efac999610b489ea1f2b2d30ea0a2f1
    """

    def __init__(self,
                 url: str,
                 key: str,
                 payload: Payload,
                 method: str = 'POST',
                 timeout: float = 60.0):
        """
        Creates a webhook request

        Parameters
        ----------

        - url: URL to call
        - key: Authorization key
        - payload: JSON payload to consider
        - method: which method to use for request. Defaults to POST
        - timeout: sets request timeout. Defauls to 60 seconds

        Exceptions
        ----------

        Raises IOError if something goes wrong.
        """
        self.url = url
        self.key = key
        self.timeout = timeout
        self.payload = payload
        self.method = method

    def send(self):
        """
        Sends the request.
        """
        headers = {
            'Authorization': self.key
        }
        try:
            response: Response = request(
                self.method,
                url=self.url,
                json=self.payload,
                timeout=self.timeout,
                headers=headers
            )
            if not response.ok:
                raise IOError(
                    f'Failed to call webhook. Code: {response.status_code} '
                    f'Content: {response.text}'
                )
        except RequestException as excpt:
            raise IOError('Failed to complete request.') from excpt
