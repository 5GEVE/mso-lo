#!flask/bin/python
import os
import unittest
import sys
sys.path.append('../')
from app import app


class NFVOTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 200, 401, 404, headers and payload for get_nfvo_list()
    def test_get_nfvo_list_200(self):
        res = self.client().get('/nfvo')
        self.assertEqual(res.status_code, 200)

    def test_get_nfvo_list_401(self):
        res = self.client().get('/nfvo?__code=401')
        self.assertEqual(res.status_code, 401)

    def test_get_nfvo_list_404(self):
        res = self.client().get('/nfvo?__code=404')
        self.assertEqual(res.status_code, 404)

    # Check status codes 200, 401, 404, headers and payload for get_nfvo(nfvoId)
    def test_get_nfvo_200(self):
        res = self.client().get('/nfvo/nfvo_osm1?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_nfvo_404(self):
        res = self.client().get('/nfvo/nfvo_id_1_missing?__code=404')
        self.assertEqual(res.status_code, 404)

    def test_get_nfvo_401(self):
        res = self.client().get('/nfvo/nfvo_osm1?__code=401')
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
