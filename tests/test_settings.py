from unittest import TestCase
from unittest.mock import patch, Mock

from kubernetes import client

from soffos.settings import (
    get_service_url,
    K8S_CONFIG
)


class Tests(TestCase):
    @patch.object(K8S_CONFIG, 'lazy_load')
    def test_get_service_url(self, k8s_config: Mock):
        name, cluster_ip, port = 'soffos-service-example', '0.0.0.0', 80
        with patch.object(
            client.CoreV1Api,
            'list_service_for_all_namespaces',
            return_value=client.V1ServiceList(items=[
                client.V1Service(spec=client.V1ServiceSpec(
                    cluster_ip=cluster_ip,
                    ports=[client.V1ServicePort(port=port)]
                ))
            ])
        ) as k8s__list_service_for_all_namespaces:
            url = get_service_url(name)
            k8s__list_service_for_all_namespaces.assert_called_once_with(
                watch=False,
                field_selector='metadata.name=' + name
            )
        k8s_config.assert_called_once()
        self.assertEqual(url, f'http://{cluster_ip}:{port}/')
