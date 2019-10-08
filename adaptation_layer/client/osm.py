import requests
import json as JSON
import yaml as YAML
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Client(object):
    def __init__(
        self,
        host=None,
        so_port=9999,
        user='admin',
        password='admin',
        project='admin', **kwargs):

        self._token_endpoint = 'admin/v1/tokens'
        self._user_endpoint = 'admin/v1/users'
        self._host = host
        self._so_port = so_port
        self._user = user
        self._password = password
        self._project = project
        self._base_path = 'https://{0}:{1}/osm'.format(self._host, so_port)
        self._headers = {"Content-Type": "application/yaml", "accept": "application/json"}
        token = self.authenticate()
        if 'error' in token:
            raise Exception(token['error'])
        self._headers['Authorization'] = 'Bearer {}'.format(token['data']['id'])

    def _exec_get(self, url=None, params=None, headers=None):
        print(headers)
        result = {}
        try:
            r = requests.get(url, params=params, verify=False, stream=True, headers=headers)
        except Exception as e:
            result['error'] = str(e)
            return result

        if r.status_code in (200, 201, 202, 204):
            if 'application/json' == r.headers['content-type']:
                result['data'] = r.json()
            elif 'application/yaml' == r.headers['content-type']:
                result['data'] = JSON.load(JSON.dumps(YAML.load(r.text), sort_keys=True, indent=2))
            else:
                result['data'] = r.text
        else:
            if 'application/json' == r.headers['content-type']:
                result['error'] = r.json()
            elif 'application/yaml' == r.headers['content-type']:
                result['error'] = JSON.loads(JSON.dumps(YAML.load(r.text), sort_keys=True, indent=2))
            else:
                result['error'] = r.text

        return result

    def _exec_post(self, url=None, data=None, json=None, headers=None):

        result = {}
        try:
            r = requests.post(url, data=data, json=json, verify=False, headers=headers)
        except Exception as e:
            result['error'] = str(e)
            return result
        if r.status_code in (200, 201, 202, 204):
            if 'application/json' == r.headers['content-type']:
                result['data'] = r.json()
            elif 'application/yaml' == r.headers['content-type']:
                result['data'] = JSON.loads(JSON.dumps(YAML.load(r.text), sort_keys=True, indent=2))
            else:
                result['data'] = r.text
        else:
            result['error'] = r.text

        return result

    def authenticate(self):
        auth_payload = {'username': self._user, 'password': self._password, 'project_id': self._project}
        token_url = "{0}/{1}".format(self._base_path, self._token_endpoint)
        return self._exec_post(token_url, json=auth_payload)

    def ns_list(self):
        _url = "{0}/nslcm/v1/ns_instances_content".format(self._base_path)
        return self._exec_get(_url, headers=self._headers)

    def vnf_list(self):
        _url = "{0}/nslcm/v1/vnfrs".format(self._base_path)
        return self._exec_get(_url, headers=self._headers)

    def ns_create(self, ns_data):
        _url = "{0}/nslcm/v1/ns_instances_content".format(self._base_path)
        return self._exec_post(_url, json=ns_data, headers=self._headers)

    def ns_op_list(self, id):
        _url = "{0}/nslcm/v1/ns_lcm_op_occs/?nsInstanceId={1}".format(
            self._base_path, id)
        return self._exec_get(_url, headers=self._headers)

    def ns_op(self, id):
        _url = "{0}/nslcm/v1/ns_lcm_op_occs/{1}".format(self._base_path, id)
        return self._exec_get(_url, headers=self._headers)

    def ns_action(self, ns_id, action_payload):
        _url = "{0}/nslcm/v1/ns_instances/{1}/action".format(self._base_path, ns_id)
        return self._exec_post(_url, json=action_payload, headers=self._headers)

    def ns_scale(self, ns_id, scale_payload):
        _url = "{0}/nslcm/v1/ns_instances/{1}/scale".format(self._base_path, ns_id)
        return self._exec_post(_url, json=scale_payload, headers=self._headers)

    def ns_delete(self, ns_id, force=None):
        result = {}
        query_path = ''
        if force:
            query_path = '?FORCE=true'
        _url = "{0}/nslcm/v1/ns_instances_content/{1}{2}".format(
            self._base_path, ns_id, query_path)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=self._headers)
        except Exception as e:
            result['error'] = str(e)
            return result
        if r.status_code != 204:
            result['data'] = r.json
        else:
            result['error'] = r.json
        return result

    def ns_get(self, id):
        _url = "{0}/nslcm/v1/ns_instances_content/{1}".format(
            self._base_path, id)
        return self._exec_get(_url, headers=self._headers)

    def vnf_get(self, id):
        _url = "{0}/nslcm/v1/vnfrs/{1}".format(self._base_path, id)
        return self._exec_get(_url, headers=self._headers)
