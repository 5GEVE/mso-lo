import sys
import unittest
from app import app  # co to za app ? to chyba chodzi o prism

# !AUTHORIZATION unsupported by ONAP driver!


class OnapTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client

        # scale a ns instance unsupported by ONAP driver
        # self.mock_ns_scale removed

        self.mock_ns = {
            "nsdId": "865e8db4-6f3f-4c69-bb13-ef911c1b8613",
            "nsName": "test_nsName",
            "nsDescription": "test_nsDescription"
        }

        self.mock_ns_instantiate = {
            "id": "188f120f-47c6-4368-a30c-5c862aff9aad",
            "nsInstanceDescription": "test_nsInstanceDescription",
            "nsInstanceName": "test_nsInstanceName",
            "nsState": "NOT_INSTANTIATED",
            "nsdId": "865e8db4-6f3f-4c69-bb13-ef911c1b8613",
            "vnfInstance": []
         }

        # terminate a ns instance with request body unsupported by ONAP driver
        self.mock_ns_terminate = {
            "terminationTime": "2017-07-21T17:32:28Z"
        }

    def tearDown(self):
        """teardown all initialized variables."""

    # Check status codes 200, 401, 404, headers and payload for get_ns_list()
    def test_get_ns_list_200(self):
        res = self.client().get('/nfvo/1/ns_instances?__code=200')
        self.assertEqual(res.status_code, 200)

    # def test_get_ns_list_401(self):
    #     res = self.client().get('/nfvo/1/ns_instances?__code=401')
    #     self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns()
    def test_get_ns_200(self):
        res = self.client().get(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_404(self):
        res = self.client().get(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=404')
        self.assertEqual(res.status_code, 404)

    # def test_get_ns_401(self):
    #     res = self.client().get(
    #         '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=401')
    #     self.assertEqual(res.status_code, 401)

    # Check status codes 201, 401, 404, headers and payload for create_ns()
    def test_create_ns_201(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=201', json=self.mock_ns)
        self.assertEqual(res.status_code, 201)

    def test_create_ns_400(self):
        res = self.client().post('/nfvo/1/ns_instances?__code=400', json=self.mock_ns)
        self.assertEqual(res.status_code, 400)

    # def test_create_ns_401(self):
    #     res = self.client().post('/nfvo/1/ns_instances?__code=401', json=self.mock_ns)
    #     self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for instantiate_ns()
    def test_instantiate_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=202',
                                 json=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 202)

    def test_instantiate_ns_400(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=400',
                                 json=self.mock_ns_instantiate)
        self.assertEqual(res.status_code, 400)

    # def test_instantiate_ns_401(self):
    #     res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/instantiate?__code=401',
    #                              json=self.mock_ns_instantiate)
    #     self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for terminate_ns()
    def test_terminate_ns_202(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=202',
                                 json=self.mock_ns_terminate)
        self.assertEqual(res.status_code, 202)

    def test_terminate_ns_404(self):
        res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=404',
                                 json=self.mock_ns_terminate)
        self.assertEqual(res.status_code, 404)

    # def test_terminate_ns_401(self):
    #     res = self.client().post('/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7/terminate?__code=401',
    #                              json=self.mock_ns_terminate)
    #     self.assertEqual(res.status_code, 401)

    # Check status codes 202, 401, 404, headers and payload for delete_ns()
    def test_delete_ns_202(self):
        res = self.client().delete(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=202')
        self.assertEqual(res.status_code, 202)

    def test_delete_ns_404(self):
        res = self.client().delete(
            '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=404')
        self.assertEqual(res.status_code, 404)

    # def test_delete_ns_401(self):
    #     res = self.client().delete(
    #         '/nfvo/1/ns_instances/49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7?__code=401')
    #     self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, 404, headers and payload for get_ns_lcm_op_occs_()
    def test_get_ns_lcm_op_occs_200(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=200')
        self.assertEqual(res.status_code, 200)

    def test_get_ns_lcm_op_occs_404(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=404')
        self.assertEqual(res.status_code, 404)

    # def test_get_ns_lcm_op_occs_401(self):
    #     res = self.client().get('/nfvo/1/ns_lcm_op_occs/49ccb6a2-5bcd-4f35-a2cf-7728c54c48b7?__code=401')
    #     self.assertEqual(res.status_code, 401)

    # Check status codes 200, 401, headers and payload for get_ns_lcm_op_occs_list()
    def test_get_ns_lcm_op_occs_list_200(self):
        res = self.client().get('/nfvo/1/ns_lcm_op_occs?__code=200')
        self.assertEqual(res.status_code, 200)

    # def test_get_ns_lcm_op_occs_list_401(self):
    #     res = self.client().get('/nfvo/1/ns_lcm_op_occs?__code=401')
    #     self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()