import requests
import os
from error_handler import ResourceNotFound, NsNotFound, VnfNotFound,\
    Unauthorized, BadRequest, ServerError, NsOpNotFound
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TESTING = os.environ.get("TESTING", False)
PRISM_ALIAS = os.environ.get("PRISM_ALIAS", "prism-onap")


class AgentClient(object):  # ns_instantiation_server
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
            # self._base_path = 'http://{0}:{1}'.format('127.0.0.1', self._port)  # for tests only
        else:
            self._base_path = 'http://{0}:{1}'.format(PRISM_ALIAS, 9999)

    def _exec_delete(self, url=None, params=None, headers=None):

        try:
            resp = requests.delete(url, params=params, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):  # response code 206 was added / limit to needed
            # print('response code: {}'.format(resp.status_code))  # for tests only
            return  # resp.json()  # for now ned to be commented maybe resp.text
        elif resp.status_code == 400:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise BadRequest()
        elif resp.status_code == 401:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise Unauthorized()
        elif resp.status_code == 404:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise ResourceNotFound()
        else:
            # print(resp.status_code)  # for tests only
            error = resp.json()
            raise ServerError(error)
            # raise ServerError()

    def _exec_post(self, url=None, data=None, json=None, headers=None):

        try:
            resp = requests.post(url, data=data, json=json, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):
            # print('response code: {}'.format(resp.status_code))  # for tests only
            return resp.json()
        elif resp.status_code == 400:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise BadRequest()
        elif resp.status_code == 401:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise Unauthorized()
        elif resp.status_code == 404:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise ResourceNotFound()
        else:
            if 'application/json' in resp.headers['content-type']:
                error = resp.json()
            else:
                error = resp.text
            # print(resp.status_code)  # for tests only
            raise ServerError(error)

    def _exec_get(self, url=None, params=None, headers=None):

        try:
            resp = requests.get(url, params=params, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):  # response code 206 was added
            # print('response code: {}'.format(resp.status_code))  # for tests only
            return resp.json()
        elif resp.status_code == 400:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise BadRequest()
        elif resp.status_code == 401:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise Unauthorized()
        elif resp.status_code == 404:
            # print('response code: {}'.format(resp.status_code))  # for tests only
            raise ResourceNotFound()
        else:
            print(resp.status_code)  # for tests only
            error = resp.json()
            raise ServerError(error)  # (error) added

    def ns_create(self, ns_name, args=None):
        args['payload']['serviceType'] = ns_name
        _url = '{0}/create'.format(self._base_path)
        try:
            return self._exec_post(_url, headers=self._headers, json=args['payload'])
        except BadRequest:
            raise BadRequest

        # _url = '{0}/instantiate/{1}'.format(self._base_path, ns_name)
        # return self._exec_post(_url, headers=self._headers)

    def ns_instantiate(self, ns_id, args=None):
        _url = '{0}/instantiate/{1}'.format(self._base_path, ns_id)
        # add try except block to check if the service instance exists
        # return self._exec_post(_url, json=args, headers=self._headers)  # for dev change to json=args['payload']
        try:
            return self._exec_post(_url, headers={"accept": "application/json"})  # header 'Location' here ? - didn't work
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_id)
        except BadRequest:
            raise BadRequest

    def ns_delete(self, ns_id, args=None):
        _url = '{0}/delete/{1}'.format(self._base_path, ns_id)
        try:
            return self._exec_delete(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_id)

    def ns_terminate(self, ns_id, args=None):
        _url = '{0}/terminate/{1}'.format(self._base_path, ns_id)
        try:
            return self._exec_post(_url, headers=self._headers, json=args['payload'])
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_id)

    def ns_list(self):
        _url = '{0}/instances'.format(self._base_path)
        return self._exec_get(_url, params=None, headers=self._headers)

    def ns_get(self, ns_Id, args=None):
        _url = '{0}/instances/{1}'.format(self._base_path, ns_Id)
        try:
            return self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=ns_Id)

    def get_op_list(self, args=None):
        _url = '{0}/ns_lcm_op_occs'.format(self._base_path)  # test it
        return self._exec_get(_url, params=None, headers=self._headers)

    def get_op(self, nsLcmOpId, args=None):
        _url = '{0}/ns_lcm_op_occs/{1}'.format(self._base_path, nsLcmOpId)  # fill with correct path
        try:
            return self._exec_get(_url, params=None, headers=self._headers)
        except ResourceNotFound:
            raise NsOpNotFound(ns_op_id=nsLcmOpId)


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
            resp = requests.get(url, params=params, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):  # response code 206 was added
            print('response code: {}'.format(resp.status_code))  # for tests only
            return resp.json()
        elif resp.status_code == 400:
            print('response code: {}'.format(resp.status_code))  # for tests only
            raise BadRequest()
        elif resp.status_code == 401:
            print('response code: {}'.format(resp.status_code))  # for tests only
            raise Unauthorized()
        elif resp.status_code == 404:
            print('response code: {}'.format(resp.status_code))  # for tests only
            raise ResourceNotFound()
        else:
            print(resp.status_code)  # for tests only
            error = resp.json()
            raise ServerError(error)  # (error) added
    #
    # def _exec_post(self, url=None, data=None, json=None, headers=None):
    #
    #     try:
    #         resp = requests.post(url, data=data, json=json, headers=None)
    #     except Exception as e:
    #         raise ServerError(str(e))
    #
    #     if resp.status_code in (200, 201, 202, 204, 206):
    #         return resp.json()
    #     elif resp.status_code == 400:
    #         print('response code: {}'.format(resp.status_code))  # for tests only
    #         raise BadRequest()
    #     elif resp.status_code == 401:
    #         print('response code: {}'.format(resp.status_code))  # for tests only
    #         raise Unauthorized()
    #     elif resp.status_code == 404:
    #         print('response code: {}'.format(resp.status_code))  # for tests only
    #         raise ResourceNotFound()
    #     else:
    #         error = resp.json()
    #         raise ServerError()

    # functionality moved to NS-server
    # def ns_list(self):
    #     _url = '{0}/service?relatedParty.id={1}'.format(self._base_path, self._customer)
    #     return self._exec_get(_url, params=None, headers=self._headers)

    # functionality moved to NS-server
    # def ns_get(self, ns_Id, args=None):
    #     _url = '{0}/service/{1}'.format(self._base_path, ns_Id)
    #     try:
    #         return self._exec_get(_url, headers=self._headers)
    #     except ResourceNotFound:
    #         raise NsNotFound(ns_id=ns_Id)

    def check_ns_name(self, nsd_Id, args=None):
        _url = '{0}/serviceSpecification/{1}?fields=name'.format(self._base_path, nsd_Id)
        try:
            return self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise BadRequest()

    # useless in current release
    # def check_instance_ns_name(self, ns_Id, args=None):
    #     _url = '{0}/service/{1}'.format(self._base_path, ns_Id)
    #     try:
    #         response = self._exec_get(_url, headers=self._headers)
    #         return response['serviceSpecification']['name']
    #     except ResourceNotFound:
    #         raise NsNotFound(ns_id=ns_Id)
