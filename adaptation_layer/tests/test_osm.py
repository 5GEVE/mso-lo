#!flask/bin/python
import sys
import unittest
from app import app
from jsonschema import validate, exceptions as jsv_exception
import response_schemas
import request_mock


class OSMTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 200, 401, 404, headers and payload for get_ns_list()
    def test_get_ns_list_200(self):
        res = self.client().get('/nfvo/1/ns_instances?__code=200')
        try:
            validate(res.json, response_schemas.ns_list_schema)
        except jsv_exception as e:
            self.fail(msg=e.message)
        self.assertEqual(res.status_code, 200)

    def test_get_ns_list_401(self):
        res = self.client().get('/nfvo/1/ns_instances?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns()
    def test_get_ns_200(self):
        res = self.client().get(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=200')
        try:
            validate(res.json, response_schemas.ns_schema)
        except jsv_exception as e:
            self.fail(msg=e.message)
        self.assertEqual(res.status_code, 200)

    def test_get_ns_404(self):
        res = self.client().get(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_get_ns_401(self):
        res = self.client().get(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 201, 401, 404, headers and payload for create_ns()
    def test_create_ns_201(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=201',
                                 json=request_mock.mock_ns)
        try:
            validate(res.json, response_schemas.ns_create_schema)
        except jsv_exception as e:
            self.fail(msg=e.message)
        self.assertEqual(res.status_code, 201)

    def test_create_ns_400(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=400',
                                 json=request_mock.mock_ns)
        self.assertEqual(res.status_code, 400)

    def test_create_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=401',
                                 json=request_mock.mock_ns)
        self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for instantiate_ns()
    def test_instantiate_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=202',
                                 json=request_mock.mock_ns_instantiate)
        # TODO check header
        self.assertEqual(res.status_code, 202)

    def test_instantiate_ns_400(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=400',
                                 json=request_mock.mock_ns_instantiate)
        self.assertEqual(res.status_code, 400)

    def test_instantiate_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=401',
                                 json=request_mock.mock_ns_instantiate)
        self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for terminate_ns()
    def test_terminate_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=202',
                                 json=request_mock.mock_ns_terminate)
        # TODO check header
        self.assertEqual(res.status_code, 202)

    def test_terminate_ns_404(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=404',
                                 json=request_mock.mock_ns_terminate)
        self.assertEqual(res.status_code, 404)

    def test_terminate_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=401',
                                 json=request_mock.mock_ns_terminate)
        self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for delete_ns()
    def test_delete_ns_202(self):
        res = self.client().delete(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=202')
        self.assertEqual(res.status_code, 202)

    def test_delete_ns_404(self):
        res = self.client().delete(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_delete_ns_401(self):
        res = self.client().delete(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for scale_ns()
    def test_scale_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/scale?__code=202',
                                 json=request_mock.mock_ns_scale)
        # TODO check header
        self.assertEqual(res.status_code, 202)

    def test_scale_ns_404(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/scale?__code=404',
                                 json=request_mock.mock_ns_scale)
        self.assertEqual(res.status_code, 404)

    def test_scale_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/scale?__code=401',
                                 json=request_mock.mock_ns_scale)
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns_lcm_op_occs_()
    def test_get_ns_lcm_op_occs_200(self):
        res = self.client().get(
            '/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=200')
        try:
            validate(res.json, response_schemas.ns_lcm_op_occ_schema)
        except jsv_exception as e:
            self.fail(msg=e.message)
        self.assertEqual(res.status_code, 200)

    def test_get_ns_lcm_op_occs_404(self):
        res = self.client().get(
            '/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_get_ns_lcm_op_occs_401(self):
        res = self.client().get(
            '/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, headers and payload for get_ns_lcm_op_occs_list()
    def test_get_ns_lcm_op_occs_list_200(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_lcm_op_occs_list_401(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs?__code=401')
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
