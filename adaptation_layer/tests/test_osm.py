#!flask/bin/python

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
from urllib.parse import urlparse

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

from app import app
from .request_mock import mock_ns, mock_ns_scale, mock_ns_terminate
from .response_schemas import ns_lcm_op_occ_schema, ns_list_schema, ns_schema, \
    ns_lcm_op_occ_list_schema


class OSMTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 201, 401, 404, headers and payload for create_ns()
    def test_create_ns_201(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=201', json=mock_ns)
        self.assertEqual(201, res.status_code)

        self.assertIn('Location', res.headers)
        validate_url = urlparse(res.headers["Location"])
        self.assertTrue(all([validate_url.scheme, validate_url.netloc, validate_url.path]))

        try:
            validate(res.json, ns_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)

    def test_create_ns_400(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=400', json=mock_ns)
        self.assertEqual(400, res.status_code)

    def test_create_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=401', json=mock_ns)
        self.assertEqual(401, res.status_code)

    # Check status codes 200, 401, 404, headers and payload for get_ns_list()
    def test_get_ns_list_200(self):
        res = self.client().get('/nfvo/1/ns_instances?__code=200')
        self.assertEqual(200, res.status_code)

        try:
            validate(res.json, ns_list_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)

    def test_get_ns_list_401(self):
        res = self.client().get('/nfvo/1/ns_instances?__code=401')
        self.assertEqual(401, res.status_code)

    # Check status codes 200, 401, 404, headers and payload for get_ns()
    def test_get_ns_200(self):
        res = self.client().get('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=200')
        self.assertEqual(200, res.status_code)

        try:
            validate(res.json, ns_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)

    def test_get_ns_404(self):
        res = self.client().get('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=404')
        self.assertEqual(404, res.status_code)

    def test_get_ns_401(self):
        res = self.client().get('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=401')
        self.assertEqual(401, res.status_code)

    # Check status codes 204, 401, 404, headers and payload for delete_ns()
    def test_delete_ns_204(self):
        res = self.client().delete('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=204')
        self.assertEqual(204, res.status_code)

    def test_delete_ns_404(self):
        res = self.client().delete('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=404')
        self.assertEqual(404, res.status_code)

    def test_delete_ns_401(self):
        res = self.client().delete('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=401')
        self.assertEqual(401, res.status_code)

    # Check status codes 202, 401, 404, headers and payload for instantiate_ns()
    def test_instantiate_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=202')
        self.assertEqual(202, res.status_code)

        self.assertIn('Location', res.headers)
        validate_url = urlparse(res.headers["Location"])
        self.assertTrue(all([validate_url.scheme, validate_url.netloc, validate_url.path]))

    def test_instantiate_ns_400(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=400')
        self.assertEqual(400, res.status_code)

    def test_instantiate_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=401')
        self.assertEqual(401, res.status_code)

    # Check status codes 202, 401, 404, headers and payload for terminate_ns()
    def test_terminate_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=202',
                                 json=mock_ns_terminate)
        self.assertEqual(202, res.status_code)

        self.assertIn('Location', res.headers)
        validate_url = urlparse(res.headers["Location"])
        self.assertTrue(all([validate_url.scheme, validate_url.netloc, validate_url.path]))

    def test_terminate_ns_404(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=404',
                                 json=mock_ns_terminate)
        self.assertEqual(404, res.status_code)

    def test_terminate_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=401',
                                 json=mock_ns_terminate)
        self.assertEqual(401, res.status_code)

    # Check status codes 202, 401, 404, headers and payload for scale_ns()
    def test_scale_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/scale?__code=202',
                                 json=mock_ns_scale)
        self.assertEqual(202, res.status_code)

        self.assertIn('Location', res.headers)
        validate_url = urlparse(res.headers["Location"])
        self.assertTrue(all([validate_url.scheme, validate_url.netloc, validate_url.path]))

    def test_scale_ns_404(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/scale?__code=404',
                                 json=mock_ns_scale)
        self.assertEqual(404, res.status_code)

    def test_scale_ns_401(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/scale?__code=401',
                                 json=mock_ns_scale)
        self.assertEqual(401, res.status_code)

    # Check status codes 200, 401, headers and payload for get_ns_lcm_op_occs_list()
    def test_get_ns_lcm_op_occs_list_200(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs?__code=200')
        self.assertEqual(200, res.status_code)

        try:
            validate(res.json, ns_lcm_op_occ_list_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)

    def test_get_ns_lcm_op_occs_list_200_filter(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs?nsInstanceId=1de0e9c3-b238-44da-b01b-b249a7784b03&__code=200')
        self.assertEqual(200, res.status_code)

        try:
            validate(res.json, ns_lcm_op_occ_list_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)

    def test_get_ns_lcm_op_occs_list_401(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs?__code=401')
        self.assertEqual(401, res.status_code)

    # Check status codes 200, 401, 404, headers and payload for get_ns_lcm_op_occs_()
    def test_get_ns_lcm_op_occs_200(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=200')
        self.assertEqual(200, res.status_code)

        try:
            validate(res.json, ns_lcm_op_occ_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)
        self.assertEqual(200, res.status_code)

    def test_get_ns_lcm_op_occs_404(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=404')
        self.assertEqual(404, res.status_code)

    def test_get_ns_lcm_op_occs_401(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=401')
        self.assertEqual(401, res.status_code)


if __name__ == '__main__':
    unittest.main()
