from unittest import TestCase
from unittest.mock import patch, Mock

from kubernetes import client

from soffos.settings import (
    get_service_url,
    K8S_CONFIG
)


class Tests(TestCase):
    @patch.object(K8S_CONFIG, 'lazy_load')
    @patch.object(
        client.CoreV1Api,
        'list_service_for_all_namespaces',
        return_value=client.V1ServiceList(items=[
            client.V1Service(spec=client.V1ServiceSpec(
                cluster_ip='0.0.0.0',
                ports=[client.V1ServicePort(port=80)]
            ))
        ])
    )
    def test_get_service_url(
        self,
        k8s__list_service_for_all_namespaces: Mock,
        k8s_config: Mock
    ):
        name = 'soffos-service'
        url = get_service_url(name)

        k8s_config.assert_called_once()
        k8s__list_service_for_all_namespaces.assert_called_once_with(
            field_selector='metadata.name=' + name
        )

        service_spec: client.V1ServiceSpec = k8s__list_service_for_all_namespaces\
            .return_value\
            .items[0]\
            .spec
        self.assertEqual(url, f'http://{service_spec.cluster_ip}:{service_spec.ports[0].port}/')

    @patch.object(K8S_CONFIG, 'lazy_load')
    @patch.object(
        client.CoreV1Api,
        'list_service_for_all_namespaces',
        return_value=client.V1ServiceList(items=[])
    )
    def test_get_service_url__name_does_not_exist(
        self,
        k8s__list_service_for_all_namespaces: Mock,
        k8s_config: Mock
    ):
        name = 'soffos-service'
        with self.assertRaises(NameError):
            get_service_url(name)

        k8s_config.assert_called_once()
        k8s__list_service_for_all_namespaces.assert_called_once_with(
            field_selector='metadata.name=' + name
        )
