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

import json
import unittest
from app import app


class NFVOTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        with open('seed/nfvo_mock.json', 'r') as f:
            self.mock_nfvo_list = json.load(f)
        self.mock_nfvo = self.mock_nfvo_list[0]

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 200, 401, 404, headers and payload for get_nfvo_list()
    def test_get_nfvo_list_200(self):
        res = self.client().get('/nfvo')
        self.assertEqual(res.status_code, 200)
        for nfvo in res.json:
            del nfvo['created_at']
            del nfvo['updated_at']
        self.assertCountEqual(self.mock_nfvo_list, res.json)

    @unittest.skip('skip 401 test as we do not have authorization yet')
    def test_get_nfvo_list_401(self):
        res = self.client().get('/nfvo?__code=401')
        self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_nfvo(nfvoId)
    def test_get_nfvo_200(self):
        res = self.client().get('/nfvo/1')
        self.assertEqual(res.status_code, 200)
        del res.json['created_at']
        del res.json['updated_at']
        self.assertDictEqual(self.mock_nfvo, res.json)

    def test_get_nfvo_404(self):
        res = self.client().get('/nfvo/-1')
        self.assertEqual(res.status_code, 404)

    @unittest.skip('skip 401 test as we do not have authorization yet')
    def test_get_nfvo_401(self):
        res = self.client().get('/nfvo/nfvo_osm1?__code=401')
        self.assertEqual(res.status_code, 401)
