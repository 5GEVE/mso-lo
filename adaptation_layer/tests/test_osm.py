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

    # Check status codes 200, 401, 404, headers and payload for get_vnf_list()
    def test_get_vnf_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_vnf_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_vnf(vnfId)
    def test_get_vnf_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf/vnf_id_1?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_vnf_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf/vnf_id_1_missing?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_get_vnf_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/vnf/vnf_id_1?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns_list()
    def test_get_ns_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 201, 401, 404, headers and payload for create_ns()
    def test_create_ns_201(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns?__code=201', data=self.mock_ns)
        self.assertEqual(res.status_code, 201)

    def test_create_ns_400(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns?__code=400', data=self.mock_ns_bad)
        self.assertEqual(res.status_code, 400)

    def test_create_ns_401(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns?__code=401', data=self.mock_ns)
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns()
    def test_get_ns_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1?__code=404')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1_missing?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_get_ns_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1?__code=404')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for instantiate_ns()
    def test_instantiate_ns_201(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate?__code=201',
                                data=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 201)

    def test_instantiate_ns_400(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate?__code=400',
                                data=self.mock_ns_instantiate_bad)
        self.assertEqual(res.status_code, 400)

    def test_instantiate_ns_401(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate?__code=401',
                                data=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for terminate_ns()
    def test_terminatee_ns_201(self):
        res = self.client().delete('/nfvo/nfvo_osm1/ns/ns_id_1/terminate?__code=201')
        self.assertEqual(res.status_code, 201)

    def test_terminate_ns_404(self):
        res = self.client().delete('/nfvo/nfvo_osm1/ns/ns_id_1/terminate?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_terminate_ns_401(self):
        res = self.client().delete('/nfvo/nfvo_osm1/ns/ns_id_1/terminate?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for scale_ns()
    def test_scale_ns_201(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/scale?__code=201',
                                data=self.mock_ns_scale)
        self.assertEqual(res.status_code, 201)

    def test_scale_ns_404(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/scale?__code=404',
                                data=self.mock_ns_scale)
        self.assertEqual(res.status_code, 404)

    def test_scale_ns_401(self):
        res = self.client().put('/nfvo/nfvo_osm1/ns/ns_id_1/scale?__code=401',
                                data=self.mock_ns_scale)
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()