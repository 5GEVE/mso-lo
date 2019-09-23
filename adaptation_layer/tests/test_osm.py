#!flask/bin/python
import os
import unittest
import sys
sys.path.append('../')
from app import app


class OSMTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.mock_nsd = {}
        self.mock_nsd_bad = {}
        self.mock_ns_scale = {}
        self.mock_ns = {}
        self.mock_ns_bad = {}
        self.mock_ns_instantiate = {}
        self.mock_ns_instantiate_bad = {}

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 200, 401, 404, headers and payload for get_nsd_list()
    def test_get_nsd_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/nsd')
        self.assertEqual(res.status_code, 200)

    def test_get_nsd_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/nsd')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_nsd(nsd_id)
    def test_get_nsd_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/nsd/nsd_id_1')
        self.assertEqual(res.status_code, 200)

    def test_get_nsd_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/nsd/nsd_id_1_missing')
        self.assertEqual(res.status_code, 404)

    def test_get_nsd_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/nsd/nsd_id_1')
        self.assertEqual(res.status_code, 401)

    # Check status codes 201, 400, 401, headers and payload for onboard_nsd()
    def test_onboard_nsd_201(self):
        res = self.client().post('/nfvo/nfvo_osm1/nsd', data=self.mock_nsd)
        self.assertEqual(res.status_code, 200)

    def test_onboard_nsd_400(self):
        res = self.client().post('/nfvo/nfvo_osm1/nsd', data=self.mock_nsd_bad)
        self.assertEqual(res.status_code, 400)

    def test_onboard_nsd_401(self):
        res = self.client().post('/nfvo/nfvo_osm1/nsd', data=self.mock_nsd)
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 400, 401, 404, headers and payload for update_nsd(nsd_info_id)
    def test_update_nsd_200(self):
        res = self.client().put('/nfvo/nfvo_osm1/nsd/nsd_id_1',
                                data=self.mock_nsd)
        self.assertEqual(res.status_code, 200)

    def test_update_nsd_404(self):
        res = self.client().put('/nfvo/nfvo_osm1/nsd/nsd_id_1_missing',
                                data=self.mock_nsd)
        self.assertEqual(res.status_code, 404)

    def test_update_nsd_401(self):
        res = self.client().put('/nfvo/nfvo_osm1/nsd/nsd_id_1',
                                data=self.mock_nsd)
        self.assertEqual(res.status_code, 401)
    # Check status codes 200, 401, 404, headers and payload for delete_nsd(nsd_id)

    def test_delete_nsd_200(self):
        res = self.client().delete('/nfvo/nfvo_osm1/nsd/nsd_id_1')
        self.assertEqual(res.status_code, 200)

    def test_delete_nsd_404(self):
        res = self.client().delete('/nfvo/nfvo_osm1/nsd/nsd_id_1_missing')
        self.assertEqual(res.status_code, 404)

    def test_delete_nsd_401(self):
        res = self.client().delete('/nfvo/nfvo_osm1/nsd/nsd_id_1')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_vnfd_list()
    def test_get_vnfd_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnfd')
        self.assertEqual(res.status_code, 200)

    def test_get_vnfd_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnfd')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_vnfd(vnfd_id)
    def test_get_vnfd_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnfd/vnfd_id_1')
        self.assertEqual(res.status_code, 200)

    def test_get_vnfd_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnfd/vnfd_id_1_missing')
        self.assertEqual(res.status_code, 404)

    def test_get_vnfd_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnfd/vnfd_id_1')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_pnfd_list()
    def test_get_pnfd_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/pnfd')
        self.assertEqual(res.status_code, 200)

    def test_get_pnfd_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/pnfd')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_pnfd(pnfd_id)
    def test_get_pnfd_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/pnfd/pnfd_id_1')
        self.assertEqual(res.status_code, 200)

    def test_get_pnfd_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/pnfd/pnfd_id_1_missing')
        self.assertEqual(res.status_code, 404)

    def test_get_pnfd_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/pnfd/pnfd_id_1')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_vnf_list()
    def test_get_vnf_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf')
        self.assertEqual(res.status_code, 200)

    def test_get_vnf_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_vnf(vnfId)
    def test_get_vnf_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf/vnf_id_1')
        self.assertEqual(res.status_code, 200)

    def test_get_vnf_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf/vnf_id_1_missing')
        self.assertEqual(res.status_code, 404)

    def test_get_vnf_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf/vnf_id_1')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns_list()
    def test_get_ns_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns')
        self.assertEqual(res.status_code, 401)

    # Check status codes 201, 401, 404, headers and payload for create_ns()
    def test_create_ns_201(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns', data=self.mock_ns)
        self.assertEqual(res.status_code, 201)

    def test_create_ns_400(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns', data=self.mock_ns_bad)
        self.assertEqual(res.status_code, 400)

    def test_create_ns_401(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns', data=self.mock_ns)
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns()
    def test_get_ns_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1_missing')
        self.assertEqual(res.status_code, 404)

    def test_get_ns_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for instantiate_ns()
    def test_instantiate_ns_201(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate',
                                data=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 201)

    def test_instantiate_ns_400(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate',
                                data=self.mock_ns_instantiate_bad)
        self.assertEqual(res.status_code, 400)

    def test_instantiate_ns_401(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate',
                                data=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for terminate_ns()
    def test_terminatee_ns_201(self):
        res = self.client().delete('/nfvo/nfvo_osm1/ns/ns_id_1/terminate')
        self.assertEqual(res.status_code, 201)

    def test_terminate_ns_404(self):
        res = self.client().delete('/nfvo/nfvo_osm1/ns/ns_id_1/terminate')
        self.assertEqual(res.status_code, 404)

    def test_terminate_ns_401(self):
        res = self.client().delete('/nfvo/nfvo_osm1/ns/ns_id_1/terminate')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for scale_ns()
    def test_scale_ns_201(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/scale',
                                data=self.mock_ns_scale)
        self.assertEqual(res.status_code, 201)

    def test_scale_ns_404(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/scale',
                                data=self.mock_ns_scale)
        self.assertEqual(res.status_code, 404)

    def test_scale_ns_401(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/scale',
                                data=self.mock_ns_scale)
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
