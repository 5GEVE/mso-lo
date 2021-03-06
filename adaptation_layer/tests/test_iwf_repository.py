#  Copyright 2019 CNIT, Francesco Lombardo, Matteo Pergolesi
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import unittest

from adaptation_layer.error_handler import VimNetworkNotFound
from adaptation_layer.repository.iwf_repository import get_nfvo_by_id, \
    get_rano_by_id, \
    get_nfvo_cred, get_rano_cred, add_orc_cred_test, get_nfvo_list, \
    get_rano_list, create_subscription, delete_subscription, get_subscription, \
    get_subscription_list, \
    search_subs_by_ns_instance, find_nfvos_by_type, post_vim_safe, \
    get_site_network, add_network_test


class TestIwfRepository(unittest.TestCase):
    """
    To run these tests you need to set the following environment variables:
    IWFREPO=true
    IWFREPO_HOST=localhost
    and have a iwf-repository instance running locally.
    """

    nfvo_id = 1
    rano_id = 1
    ns_instance = "45f95003-4dd1-4e20-87cf-4373c9f4e946"
    sub_id = ""
    net_name = "osm-external"
    net_site = 1

    @classmethod
    def setUpClass(cls) -> None:
        add_orc_cred_test('nfvo', cls.nfvo_id)
        add_orc_cred_test('rano', cls.rano_id)
        sub = {
            "callbackUri": "http://127.0.0.1:8082/",
            "nsInstanceId": cls.ns_instance,
            "notificationTypes": [
                "NsLcmOperationOccurrenceNotification",
                "NsIdentifierDeletionNotification",
                "NsIdentifierCreationNotification"
            ]
        }
        cls.sub_id = create_subscription(cls.nfvo_id, sub)['id']
        site_network = {
            "vim_network_name": cls.net_name,
            "floating_ip": True,
            "mgmt_net": False,
            "external_net": True,
            "cidr": "10.100.1.0/24",
            "ip_mapping": None,
        }
        add_network_test(site_network, cls.net_site)

    def test_get_nfvo_by_id(self):
        nfvo = get_nfvo_by_id(TestIwfRepository.nfvo_id)
        self.assertEqual({'id': 1, 'name': 'ITALY_TURIN', 'site': 'ITALY_TURIN', 'type': 'OSM'}, nfvo)

    def test_get_rano_by_id(self):
        rano = get_rano_by_id(self.rano_id)
        self.assertEqual({'id': 1, 'name': 'ITALY_EVER', 'site': 'ITALY_TURIN', 'type': 'EVER'}, rano)

    def test_get_nfvo_cred(self):
        cred = get_nfvo_cred(self.nfvo_id)
        self.assertEqual({'host': '192.168.1.2',
                          'nfvo_id': 1,
                          'password': 'admin',
                          'port': 9999,
                          'project': 'admin',
                          'user': 'admin'}, cred)

    def test_get_rano_cred(self):
        cred = get_rano_cred(self.rano_id)
        self.assertEqual({'host': '192.168.1.2',
                          'rano_id': 1,
                          'password': 'admin',
                          'port': 9999,
                          'project': 'admin',
                          'user': 'admin'}, cred)

    def test_get_nfvo_list(self):
        length = len(get_nfvo_list())
        self.assertEqual(10, length)

    def test_get_rano_list(self):
        length = len(get_rano_list())
        self.assertEqual(1, length)

    def test_get_subscription(self):
        sub = get_subscription(self.nfvo_id, self.sub_id)
        expected = {'_links': {'lccnSubscription': {'href': 'http://localhost:8087/subscriptions/19'},
                               'nfvOrchestrators': {'href': 'http://localhost:8087/subscriptions/19/nfvOrchestrators'},
                               'self': {'href': 'http://localhost:8087/subscriptions/19'}},
                    'callbackUri': 'http://127.0.0.1:8082/',
                    'id': 19,
                    'notificationTypes': ['NsLcmOperationOccurrenceNotification',
                                          'NsIdentifierCreationNotification',
                                          'NsIdentifierDeletionNotification'],
                    'nsInstanceId': '45f95003-4dd1-4e20-87cf-4373c9f4e946'}
        self.assertEqual(expected.keys(), sub.keys())

    def test_get_subscription_list(self):
        length = len(get_subscription_list(self.nfvo_id)['_embedded']['subscriptions'])
        self.assertEqual(1, length)

    def test_search_subs_by_ns_instance(self):
        length = len(search_subs_by_ns_instance(self.ns_instance))
        self.assertEqual(1, length)

    def test_find_nfvos_by_type(self):
        length = len(find_nfvos_by_type('osm'))
        self.assertEqual(3, length)

    def test_post_vim_safe(self):
        osm_vim = {
            "vim_url": "http://10.20.20.1:5000/v3",
            "_id": "c25ce403-b664-48e3-b790-9ed7635feffc",
            "vim_tenant_name": "admin",
            "_admin": {
                "deployed": {
                    "RO": "bd440a16-91ec-11ea-9c7d-02420aff0017",
                    "RO-account": "bd52553a-91ec-11ea-9c7d-02420aff0017"
                },
                "detailed-status": "Done",
                "operationalState": "ENABLED",
                "projects_write": [
                    "3f9cef5c-b729-45a8-a9a2-e8acbb24701d"
                ],
                "projects_read": [
                    "3f9cef5c-b729-45a8-a9a2-e8acbb24701d"
                ],
                "operations": [
                    {
                        "lcmOperationType": "create",
                        "operationParams": None,
                        "worker": "a1c64c46ea60",
                        "startTime": 1589025656.1463664,
                        "statusEnteredTime": 1589025656.1463664,
                        "operationState": "COMPLETED",
                        "detailed-status": "Done"
                    }
                ],
                "modified": 1589025656.146264,
                "created": 1589025656.146264,
                "current_operation": 0
            },
            "vim_user": "admin",
            "config": {},
            "schema_version": "1.11",
            "vim_type": "openstack",
            "vim_password": "passwd",
            "name": "microstack-admin"
        }
        post_vim_safe(osm_vim, f'http://localhost:8087/nfvOrchestrators/{self.nfvo_id}')

    def test_get_site_network(self):
        net = get_site_network(self.net_name, self.nfvo_id)
        self.assertDictEqual({
            "id": 1,
            "vim_network_name": self.net_name,
            "floating_ip": True,
            "mgmt_net": False,
            "external_net": True,
            "cidr": "10.100.1.0/24",
            "ip_mapping": None,
            "_links": {
                "self": {
                    "href": "http://iwf-repository-app:8087/networks/1"
                },
                "network": {
                    "href": "http://iwf-repository-app:8087/networks/1"
                },
                "site": {
                    "href": "http://iwf-repository-app:8087/networks/1/site"
                }
            }
        }, net)

    def test_get_site_network_not_found(self):
        self.assertRaises(VimNetworkNotFound, get_site_network, 'notfound', self.nfvo_id)


if __name__ == '__main__':
    unittest.main()
