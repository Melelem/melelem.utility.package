from unittest import TestCase
from unittest.mock import patch
import os

from soffos.settings import (
    get_service_url
)


class Tests(TestCase):
    def test_get_service_url(self):
        name, host, port = 'X', 'api.soffos.ai', '80'
        env_vars = {f'{name}_SERVICE_HOST': host, f'{name}_SERVICE_PORT': port}
        with patch.dict(os.environ, env_vars):
            url = get_service_url(name)
            self.assertEqual(url, f'http://{host}:{port}/')

    def test_get_service_url__invalid_name(self):
        with self.assertRaises(NameError):
            get_service_url('SOFFOS-SERVICE')
