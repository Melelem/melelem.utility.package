import os

from kubernetes import client
from kubernetes.config import load_incluster_config

from .utilities import LazyLoader


DEBUG = bool(int(os.environ.get('DEBUG', '0')))

K8S = LazyLoader(client.CoreV1Api)
K8S_CONFIG = LazyLoader(load_incluster_config)


def get_service_url(name: str):
    """
    Get the URL of a service by name from kubernetes' internal API.

    :param name: The name of the service. E.g. 'soffos-api'.
    :raises NameError: If the service does not exist.
    :return: The service's URL.
    """
    K8S_CONFIG()

    services: client.V1ServiceList = K8S().list_service_for_all_namespaces(
        field_selector='metadata.name=' + name
    )
    if not services.items:
        raise NameError('Service does not exist.')
    service: client.V1Service = services.items[0]
    service_spec: client.V1ServiceSpec = service.spec
    service_port: client.V1ServicePort = service_spec.ports[0]

    return f'http://{service_spec.cluster_ip}:{service_port.port}/'
