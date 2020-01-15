import requests
import os
from urllib.parse import urlencode
from error_handler import ResourceNotFound, NsNotFound,\
    Unauthorized, BadRequest, ServerError, NsOpNotFound
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TESTING = os.environ.get("TESTING", False)
PRISM_ALIAS = os.environ.get("PRISM_ALIAS", "prism-onap")


# ns_instantiation_server
class AgentClient(object):
    def __init__(
            self,
            host=None,
            so_port=8080,
            **kwargs):

        self._host = host
        self._port = so_port
        self._headers = {"Content-Type": "application/json",
                         "accept": "application/json"}

        if TESTING is False:
            # self._base_path = 'http://{0}:{1}'.format(self._host, self._port)
            self._base_path = 'http://{0}:{1}'.format('10.254.184.215', self._port)  # for tests only
        else:
            self._base_path = 'http://{0}:{1}'.format(PRISM_ALIAS, 9999)

    def _exec_delete(self, url=None, params=None, headers=None):

        try:
            resp = requests.delete(url, params=params, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):
            return  # resp.json()  # for now ned to be commented maybe resp.text
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            error = resp.json()
            raise ServerError(error)

    def _exec_post(self, url=None, data=None, json=None, headers=None):

        try:
            resp = requests.post(url, data=data, json=json, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):
            return resp.json()
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            if 'application/json' in resp.headers['content-type']:
                error = resp.json()
            else:
                error = resp.text
            raise ServerError(error)

    def _exec_get(self, url=None, params=None, headers=None):

        try:
            resp = requests.get(url, params=params, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):  # response code 206 was added
            return resp.json()
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            error = resp.json()
            raise ServerError(error)  # (error) added

    def ns_create(self, ns_name, args=None):
        args['payload']['serviceType'] = ns_name
        _url = '{0}/create'.format(self._base_path)
        _url = _build_testing_url(_url, args)
        try:
            return self._exec_post(_url, headers=self._headers, json=args['payload'])
        except BadRequest:
            raise BadRequest

    def ns_instantiate(self, ns_id, args=None):
        _url = '{0}/instantiate/{1}'.format(self._base_path, ns_id)
        _url = _build_testing_url(_url, args)
        try:
            return self._exec_post(_url, headers={"accept": "application/json"})
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_id)
        except BadRequest:
            raise BadRequest

    def ns_delete(self, ns_id, args=None):
        _url = '{0}/delete/{1}'.format(self._base_path, ns_id)
        _url = _build_testing_url(_url, args)
        try:
            return self._exec_delete(_url, headers={"accept": "application/json"})
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_id)

    def ns_terminate(self, ns_id, args=None):
        _url = '{0}/terminate/{1}'.format(self._base_path, ns_id)
        _url = _build_testing_url(_url, args)
        try:
            return self._exec_post(_url, headers=self._headers, json=args['payload'])
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_id)

    def ns_list(self, args=None):
        _url = '{0}/instances'.format(self._base_path)
        _url = _build_testing_url(_url, args)
        return self._exec_get(_url, params=None, headers=self._headers)

    def ns_get(self, ns_Id, args=None):
        _url = '{0}/instances/{1}'.format(self._base_path, ns_Id)
        _url = _build_testing_url(_url, args)
        try:
            return self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_Id)

    def get_op_list(self, args=None):
        _url = '{0}/ns_lcm_op_occs'.format(self._base_path)
        _url = _build_testing_url(_url, args)
        return self._exec_get(_url, params=None, headers=self._headers)

    def get_op(self, nsLcmOpId, args=None):
        _url = '{0}/ns_lcm_op_occs/{1}'.format(self._base_path, nsLcmOpId)
        _url = _build_testing_url(_url, args)
        try:
            return self._exec_get(_url, params=None, headers=self._headers)
        except ResourceNotFound:
            raise NsOpNotFound(ns_op_id=nsLcmOpId)


# ONAP NBI api
class Client(object):
    def __init__(
            self,
            host=None,
            so_port=30274,
            **kwargs):

        self._host = host
        self._port = so_port
        self._nbi_ver = 4
        self._customer = 'generic'  # when blank, default 'generic' ; IMPORTANT!
        self._headers = {"Content-Type": "application/json",
                         "accept": "application/json"}

        if TESTING is False:
            # self._base_path = 'http://{0}:{1}/nbi/api/v{2}'.format(self._host, self._port, self._nbi_ver)
            # for tests only
            self._base_path = 'http://{0}:{1}/nbi/api/v{2}'.format('10.254.184.164', self._port, self._nbi_ver)
        else:
            self._base_path = 'http://{0}:{1}/nbi/api/v4'.format(PRISM_ALIAS, 9999)

    def _exec_get(self, url=None, params=None, headers=None):

        try:
            resp = requests.get(url, params=params, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):  # response code 206 was added
            return resp.json()
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            error = resp.json()
            raise ServerError(error)  # (error) added

    def check_ns_name(self, nsd_Id, args=None):
        _url = '{0}/serviceSpecification/{1}?fields=name'.format(self._base_path, nsd_Id)
        _url = _build_testing_url(_url, args)
        try:
            return self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise BadRequest()


def _build_testing_url(base, args):
    if TESTING and args and args['args']:
        url_query = urlencode(args['args'])
        return "{0}?{1}".format(base, url_query)
    return base
