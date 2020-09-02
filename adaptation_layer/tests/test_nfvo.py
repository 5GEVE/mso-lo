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

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

from adaptation_layer import create_app
from .response_schemas import nfvo_schema, nfvo_list_schema


class NFVOTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 200, 401, headers and payload for get_nfvo_list()
    def test_get_nfvo_list_200(self):
        res = self.client().get('/nfvo')
        self.assertEqual(200, res.status_code)
        try:
            validate(res.json, nfvo_list_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)

    @unittest.skip('skip 401 test as we do not have authorization yet')
    def test_get_nfvo_list_401(self):
        res = self.client().get('/nfvo?__code=401')
        self.assertEqual(401, res.status_code)

    # Check status codes 200, 401, 404, headers and payload for get_nfvo(nfvoId)
    def test_get_nfvo_200(self):
        res = self.client().get('/nfvo/1')
        self.assertEqual(200, res.status_code)
        try:
            validate(res.json, nfvo_schema)
        except (ValidationError, SchemaError) as e:
            self.fail(msg=e.message)

    def test_get_nfvo_404(self):
        res = self.client().get('/nfvo/-1')
        self.assertEqual(404, res.status_code)

    @unittest.skip('skip 401 test as we do not have authorization yet')
    def test_get_nfvo_401(self):
        res = self.client().get('/nfvo/nfvo_osm1?__code=401')
        self.assertEqual(401, res.status_code)
