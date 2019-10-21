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
        self.mock_ns_scale = {
            "scaleType": "SCALE_VNF",
            "scaleVnfData": {
                "scaleVnfType": "SCALE_IN",
                "scaleByStepData": {
                    "scaling-group-descriptor": "12313"
                }
            }
        }
        self.mock_ns = {
            "nsdId": "49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7",
            "nsName": "test",
            "nsDescription": "test description",
            "vimAccountId": "69ccb6a2-5bcd-4f35-a2cf-7728c54e48b7"
        }
        self.mock_ns_instantiate = {
            "nsdId": "49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7",
            "nsName": "test",
            "vimAccountId": "69ccb6a2-5bcd-4f35-a2cf-7728c54e48b7"
        }
        self.mock_ns_terminate = {
            "terminationTime": "2017-07-21T17:32:28Z"
        }

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 200, 401, 404, headers and payload for get_ns_list()
    def test_get_ns_list_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_list_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns()
    def test_get_ns_200(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_404(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1_missing?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_get_ns_401(self):
        res = self.client().get('/nfvo/nfvo_osm1/ns/ns_id_1?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 201, 401, 404, headers and payload for create_ns()
    def test_create_ns_201(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns?__code=201', json=self.mock_ns)
        self.assertEqual(res.status_code, 201)

    def test_create_ns_400(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns?__code=400', json=self.mock_ns)
        self.assertEqual(res.status_code, 400)

    def test_create_ns_401(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns?__code=401', json=self.mock_ns)
        self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for instantiate_ns()
    def test_instantiate_ns_202(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate?__code=202',
                                json=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 202)

    def test_instantiate_ns_400(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate?__code=400',
                                json=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 400)

    def test_instantiate_ns_401(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/instantiate?__code=401',
                                json=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for terminate_ns()
    def test_terminatee_ns_202(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/terminate?__code=202', json=self.mock_ns_terminate)
        self.assertEqual(res.status_code, 202)

    def test_terminate_ns_404(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/terminate?__code=404', json=self.mock_ns_terminate)
        self.assertEqual(res.status_code, 404)

    def test_terminate_ns_401(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/terminate?__code=401', json=self.mock_ns_terminate)
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for scale_ns()
    def test_scale_ns_202(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/scale?__code=200', json=self.mock_ns_scale)
        self.assertEqual(res.status_code, 202)

    def test_scale_ns_404(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/scale?__code=404', json=self.mock_ns_scale)
        self.assertEqual(res.status_code, 404)

    def test_scale_ns_401(self):
        res = self.client().post('/nfvo/nfvo_osm1/ns/ns_id_1/scale?__code=401', json=self.mock_ns_scale)
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
