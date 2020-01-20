import os
import re
from typing import Dict, Tuple, List
from urllib.parse import urlencode
import logging  # for tests only
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from error_handler import ResourceNotFound, NsNotFound,\
     BadRequest, ServerError, NsOpNotFound

from .interface import Driver, Headers, BodyList, Body

urllib3.disable_warnings(InsecureRequestWarning)
TESTING = os.environ.get("TESTING", False)
PRISM_ALIAS = os.environ.get("PRISM_ALIAS", "prism-onap")


class ONAP(Driver):

    def __init__(self, nfvo_cred):
        self._nfvoId = nfvo_cred["nfvo_id"]
        # self._onap_host = nfvo_cred["host"]
        self._onap_host = '127.0.0.1'  # '10.254.184.164'  # for tests only
        self._ns_host = '127.0.0.1'  # '10.254.184.215'  # for tests only
        self._onap_port = nfvo_cred["port"] if "port" in nfvo_cred else 30274
        self._ns_port = 8080
        self._nbi_ver = 4
        self._customer = 'generic'  # when blank, default 'generic' ; IMPORTANT!
        self._headers = {"Content-Type": "application/json",
                         "Accept": "application/json"}

        if TESTING is False:
            self._onap_base_path = 'http://{0}:{1}/nbi/api/v{2}'.format(
                self._onap_host, self._onap_port, self._nbi_ver)
            self._ns_base_path = 'http://{0}:{1}'.format(self._ns_host, self._ns_port)
        else:
            self._onap_base_path = 'http://{0}:{1}/nbi/api/v4'.format(PRISM_ALIAS, 9999)
            self._ns_base_path = 'http://{0}:{1}'.format(PRISM_ALIAS, 9999)

    def _exec_delete(self, url=None, params=None, headers=None):

        try:
            resp = requests.delete(url, params=params, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 204, 206):
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), resp.headers
            else:
                return resp.text, resp.headers
        elif resp.status_code == 400:
            raise BadRequest()
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
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), resp.headers
            else:
                return resp.text, resp.headers
        elif resp.status_code == 400:
            raise BadRequest()
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
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), resp.headers
            else:
                return resp.text, resp.headers
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            error = resp.json()
            raise ServerError(error)

    # all methods

    def get_ns_list(self, args=None) -> Tuple[BodyList, Headers]:
        _url = '{0}/instances'.format(self._ns_base_path)
        _url = self._build_url_query(_url, args)
        ns_list, resp_headers = self._exec_get(_url, headers=self._headers)
        headers = self._build_headers(resp_headers)
        return ns_list, headers

    def create_ns(self, args=None) -> Tuple[Body, Headers]:
        # check the name od nsdId
        nsd_Id = args['payload']['nsdId']
        _url = '{0}/serviceSpecification/{1}?fields=name'.format(self._onap_base_path, nsd_Id)
        _url = self._build_url_query(_url, args)
        try:
            response = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise BadRequest()
        # add serviceType from response to args
        ns_name = response[0]['name']  # TODO test it!
        args['payload']['serviceType'] = ns_name
        # create ns instance
        _url = '{0}/create'.format(self._ns_base_path)
        _url = self._build_url_query(_url, args)
        created_ns, resp_headers = self._exec_post(
            _url, json=args['payload'], headers=self._headers)
        headers = self._build_headers(resp_headers)
        return created_ns, headers

    def get_ns(self, nsId: str, args=None, skip_sol=False) -> Tuple[Body, Headers]:
        _url = '{0}/instances/{1}'.format(self._ns_base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            ns_instance, resp_headers = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return ns_instance, headers

    def delete_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
        _url = '{0}/delete/{1}'.format(self._ns_base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            empty_body, resp_headers = self._exec_delete(
                _url, params=None, headers={"Accept": "application/json"})
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return None, headers

    def instantiate_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        _url = '{0}/instantiate/{1}'.format(self._ns_base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            empty_body, resp_headers = self._exec_post(
                _url, headers={"Accept": "application/json"})
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return None, headers

    def terminate_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        _url = '{0}/terminate/{1}'.format(self._ns_base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            emtpy_body, resp_headers = self._exec_post(
                _url, json=args['payload'], headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return None, headers

    def scale_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        pass

    def get_op_list(self, args: Dict = None) -> Tuple[BodyList, Headers]:
        nsId = args['args']['nsInstanceId'] if args['args'] and 'nsInstanceId' in args['args'] else None
        # _url = "{0}/ns_lcm_op_occs".format(self._ns_base_path)
        # _url = self._build_url_query(_url, args)
        logging.error(nsId)
        if nsId is None:
            _url = "{0}/ns_lcm_op_occs".format(self._ns_base_path)
            _url = self._build_url_query(_url, args)
            op_list, resp_headers = self._exec_get(_url, headers=self._headers)
        else:
            _url = "{0}/ns_lcm_op_occs/ns_id/{1}".format(self._ns_base_path, nsId)
            _url = self._build_url_query(_url, args)
            try:
                op_list, resp_headers = self._exec_get(_url, headers=self._headers)
            except ResourceNotFound:
                raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return op_list, headers

        # doesn't support filtering
        # _url = '{0}/ns_lcm_op_occs'.format(self._ns_base_path)
        # _url = self._build_url_query(_url, args)
        # op_list, resp_headers = self._exec_get(_url, headers=self._headers)
        # headers = self._build_headers(resp_headers)
        # return op_list, headers

    def get_op(self, nsLcmOpId, args: Dict = None) -> Tuple[Body, Headers]:
        _url = '{0}/ns_lcm_op_occs/lcm_id/{1}'.format(self._ns_base_path, nsLcmOpId)
        _url = self._build_url_query(_url, args)
        try:
            lcm_op, resp_headers = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsOpNotFound(ns_op_id=nsLcmOpId)
        headers = self._build_headers(resp_headers)
        return lcm_op, headers

    #
    @staticmethod
    def _build_url_query(base, args):
        if args and args['args']:
            url_query = urlencode(args['args'])
            return "{0}?{1}".format(base, url_query)
        return base

    def _build_headers(self, resp_headers):
        headers = {}
        if 'location' in resp_headers:
            re_res = re.findall(
                r"/ns-server/(ns_db_id|ns_lcm_op_occs)/([A-Za-z0-9\-]+)", resp_headers['location'])
            if len(re_res):
                if re_res[0][0] == 'ns_db_id':
                    headers['location'] = '/nfvo/{0}/ns_instances/{1}'.format(
                        self._nfvoId, re_res[0][1])
                elif re_res[0][0] == 'ns_lcm_op_occs':
                    headers['location'] = '/nfvo/{0}/ns_lcm_op_occs/{1}'.format(
                        self._nfvoId, re_res[0][1])
        return headers

    # old version
    #
    # def __init__(self):
    #     self._client = ONAPclient()
    #     self._agent = AGENTclient()
    #     # self._client = ONAPclient(**self)
    #
    # def create_ns(self, args: Dict = None) -> Dict:
    #     ns_name = self._client.check_ns_name(args['payload']['nsdId'])  # retrieve name of nsdId
    #     return self._agent.ns_create(ns_name['name'], args=args)
    #
    # def get_ns_list(self, args=None) -> List[Dict]:
    #     return self._agent.ns_list()
    #
    # def get_ns(self, nsId: str, args=None) -> Dict:
    #     return self._agent.ns_get(nsId, args=args)
    #
    # def delete_ns(self, nsId: str, args: Dict = None) -> None:
    #     return self._agent.ns_delete(nsId, args=args)
    #
    # def instantiate_ns(self, nsId: str, args: Dict = None) -> None:
    #     return self._agent.ns_instantiate(nsId, args=args)
    #
    # # unsupported by ONAP
    # def scale_ns(self, nsId: str, args: Dict = None) -> None:
    #     pass
    #
    # def terminate_ns(self, nsId: str, args: Dict = None) -> None:
    #     return self._agent.ns_terminate(nsId, args=args)
    #
    # def get_op_list(self, args: Dict = None) -> List[Dict]:
    #     return self._agent.get_op_list()
    #
    # def get_op(self, nsLcmOpId: str, args: Dict = None) -> Dict:
    #     return self._agent.get_op(nsLcmOpId, args=args)
    #
