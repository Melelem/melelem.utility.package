import os
import re


DEBUG = bool(int(os.environ.get('DEBUG', '0')))


def get_service_url(name: str):
    """
    Get the URL of service from the environment variables.
    https://kubernetes.io/docs/concepts/services-networking/service/#environment-variables

    :param name: The name of the service. E.g. MY_SERVICE.
    :raises NameError: If the name contains invalid characters.
    :return: The service's URL.
    """
    name = name.strip().upper()
    if re.search(r'[^A-Z0-9_]+', name):
        raise NameError('Name contains invalid characters.')

    host_key, port_key = f'{name}_SERVICE_HOST', f'{name}_SERVICE_PORT'
    host = os.environ.get(host_key, 'localhost') if DEBUG else os.environ[host_key]
    port = os.environ.get(port_key, '5000') if DEBUG else os.environ[port_key]
    return f'http://{host}:{port}/'
