import json as JSON
import os
from datetime import datetime
from typing import Dict, Tuple
from urllib.parse import urlencode

import requests
import yaml as YAML
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from error_handler import ResourceNotFound, NsNotFound, VnfNotFound, \
    Unauthorized, BadRequest, ServerError, NsOpNotFound, VnfPkgNotFound
from .interface import Driver, Headers, BodyList, Body

urllib3.disable_warnings(InsecureRequestWarning)
TESTING = os.environ.get("TESTING", False)
PRISM_ALIAS = os.environ.get("PRISM_ALIAS", "prism-osm")


class OSM(Driver):

    def __init__(self, nfvo_cred):
        self._token_endpoint = 'admin/v1/tokens'
        self._user_endpoint = 'admin/v1/users'
        self._host = nfvo_cred["host"]
        self._so_port = nfvo_cred["port"] if "port" in nfvo_cred else 9999
        self._user = nfvo_cred["user"]
        self._password = nfvo_cred["password"]
        self._project = nfvo_cred["project"]
        self._headers = {"Content-Type": "application/json",
                         "accept": "application/json"}
        if TESTING is False:
            self._base_path = 'https://{0}:{1}/osm'.format(self._host, self._so_port)
            token, headers = self._authenticate()
            self._headers['Authorization'] = 'Bearer {}'.format(token['id'])
        else:
            self._base_path = 'http://{0}:{1}/osm'.format(PRISM_ALIAS, self._so_port)

    def _exec_get(self, url=None, params=None, headers=None):
        # result = {}
        try:
            resp = requests.get(url, params=params,
                                verify=False, stream=True, headers=headers)
        except Exception as e:
            raise ServerError(str(e))
        if resp.status_code in (200, 201, 202, 204):
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), dict(**resp.headers)
            elif 'application/yaml' in resp.headers['content-type']:
                return JSON.loads(JSON.dumps(YAML.load(resp.text), sort_keys=True, indent=2)), dict(**resp.headers)
            else:
                return resp.text, dict(**resp.headers)
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            if 'application/json' in resp.headers['content-type']:
                error = resp.json()
            elif 'application/yaml' in resp.headers['content-type']:
                error = JSON.loads(JSON.dumps(
                    YAML.safe_load(resp.text), sort_keys=True, indent=2))
            else:
                error = resp.text
            raise ServerError(error)

    def _exec_post(self, url=None, data=None, json=None, headers=None):
        try:
            resp = requests.post(url, data=data, json=json,
                                 verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))
        if resp.status_code in (200, 201, 202, 204):
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), dict(**resp.headers)
            elif 'application/yaml' in resp.headers['content-type']:
                return JSON.loads(JSON.dumps(YAML.load(resp.text), sort_keys=True, indent=2)), dict(**resp.headers)
            else:
                return resp.text, dict(**resp.headers)
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            if 'application/json' in resp.headers['content-type']:
                error = resp.json()
            elif 'application/yaml' in resp.headers['content-type']:
                error = JSON.loads(JSON.dumps(YAML.safe_load(resp.text), sort_keys=True, indent=2))
            else:
                error = resp.text
            raise ServerError(error)

    def _exec_delete(self, url=None, params=None, headers=None):
        try:
            resp = requests.delete(url, params=params, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))
        if resp.status_code in (200, 201, 202, 204):
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), dict(**resp.headers)
            elif 'application/yaml' in resp.headers['content-type']:
                return JSON.loads(JSON.dumps(YAML.load(resp.text), sort_keys=True, indent=2)), dict(**resp.headers)
            else:
                return resp.text, dict(**resp.headers)
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            if 'application/json' in resp.headers['content-type']:
                error = resp.json()
            elif 'application/yaml' in resp.headers['content-type']:
                error = JSON.loads(JSON.dumps(YAML.safe_load(resp.text), sort_keys=True, indent=2))
            else:
                error = resp.text
            raise ServerError(error)

    def _authenticate(self):
        auth_payload = {'username': self._user,
                        'password': self._password,
                        'project_id': self._project}
        token_url = "{0}/{1}".format(self._base_path, self._token_endpoint)
        return self._exec_post(token_url, json=auth_payload)

    def get_vnf_list(self, args=None) -> Tuple[BodyList, Headers]:
        _url = "{0}/nslcm/v1/vnf_instances".format(self._base_path)
        _url = self._build_url_query(_url, args)
        return self._exec_get(_url, headers=self._headers)

    def get_vnf(self, vnfId: str, args=None) -> Tuple[Body, Headers]:
        _url = "{0}/nslcm/v1/vnf_instances/{1}".format(self._base_path, vnfId)
        _url = self._build_url_query(_url, args)
        try:
            return self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise VnfNotFound(vnf_id=vnfId)

    def get_vnfpkg(self, vnfPkgId, args=None):
        _url = "{0}/vnfpkgm/v1/vnf_packages/{1}".format(self._base_path, vnfPkgId)
        _url = self._build_url_query(_url, args)
        try:
            return self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise VnfPkgNotFound(vnfpkg_id=vnfPkgId)

    def get_ns_list(self, args=None) -> Tuple[BodyList, Headers]:
        _url = "{0}/nslcm/v1/ns_instances".format(self._base_path)
        _url = self._build_url_query(_url, args)
        osm_ns_list, headers = self._exec_get(_url, headers=self._headers)
        sol_ns_list = []
        for osm_ns in osm_ns_list:
            sol_ns_list.append(self._ns_im_converter(osm_ns))
        return sol_ns_list, headers

    def create_ns(self, args=None) -> Tuple[Body, Headers]:
        _url = "{0}/nslcm/v1/ns_instances".format(self._base_path)
        _url = self._build_url_query(_url, args)
        return self._exec_post(_url, json=args['payload'], headers=self._headers)

    def get_ns(self, nsId: str, args=None) -> Tuple[Body, Headers]:
        _url = "{0}/nslcm/v1/ns_instances/{1}".format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            ns, headers = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        return self._ns_im_converter(ns), headers

    def delete_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
        _url = "{0}/nslcm/v1/ns_instances/{1}".format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            ns, headers = self._exec_delete(_url, params=None, headers={"accept": "application/json"})
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        return None, headers

    def instantiate_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        _url = "{0}/nslcm/v1/ns_instances/{1}/instantiate".format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            return self._exec_post(_url, json=args['payload'], headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)

    def terminate_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        _url = "{0}/nslcm/v1/ns_instances/{1}/terminate".format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            return self._exec_post(_url, json=args['payload'], headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)

    def scale_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        _url = "{0}/nslcm/v1/ns_instances/{1}/scale".format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            return self._exec_post(_url, json=args['payload'], headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=id)

    def get_op_list(self, args: Dict = None) -> Tuple[BodyList, Headers]:
        nsId = args['args']['nsInstanceId'] if args['args'] and 'nsInstanceId' in args['args'] else None
        _url = "{0}/nslcm/v1/ns_lcm_op_occs".format(self._base_path)
        _url = self._build_url_query(_url, args)
        try:
            osm_op_list, headers = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        sol_op_list = []
        for op in osm_op_list:
            sol_op_list.append(self._op_im_converter(op))
        return sol_op_list, headers

    def get_op(self, nsLcmOpId, args: Dict = None) -> Tuple[Body, Headers]:
        _url = "{0}/nslcm/v1/ns_lcm_op_occs/{1}".format(self._base_path, nsLcmOpId)
        _url = self._build_url_query(_url, args)
        try:
            op, headers = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsOpNotFound(ns_op_id=nsLcmOpId)
        return self._op_im_converter(op), headers

    def _cpinfo_converter(self, osm_vnf):
        cp_info = []
        try:
            vnfpkg, headers = self.vnfpkg_get(osm_vnf["vnfd-id"])
        except VnfPkgNotFound:
            return cp_info
        for vdur in osm_vnf["vdur"]:
            for if_vdur in vdur["interfaces"]:
                [if_pkg] = [if_pkg for vdu in vnfpkg["vdu"] for if_pkg in vdu["interface"]
                            if vdu["id"] == vdur["vdu-id-ref"] and if_pkg["name"] == if_vdur["name"]]
                [cp] = [val for key, val in if_pkg.items() if key.endswith("-connection-point-ref")]
                try:
                    (ip_address, mac_address) = (if_vdur["ip_address"], if_vdur["mac_address"])
                except KeyError:
                    (ip_address, mac_address) = (None, None)
                cp_info.append({
                    "id": cp,
                    "cpProtocolInfo": [
                        {
                            "layerProtocol": "IP_OVER_ETHERNET",
                            "ipOverEthernet": {
                                "macAddress": mac_address,
                                "ipAddresses": [
                                    {
                                        "type": "IPV4",
                                        "addresses": [ip_address]
                                    }
                                ]
                            }
                        }
                    ]
                })

    def _ns_im_converter(self, osm_ns: Dict) -> Dict:
        sol_ns = {
            "id": osm_ns['id'],
            "nsInstanceName": osm_ns['name'],
            "nsInstanceDescription": osm_ns['description'],
            "nsdId": osm_ns['nsd-id'],
            "nsState": osm_ns['_admin']['nsState'],
            "vnfInstance": []
        }

        osm_vnfs = []
        if 'constituent-vnfr-ref' in osm_ns:
            for vnf_id in osm_ns["constituent-vnfr-ref"]:
                try:
                    vnf, headers = self.get_vnf(vnf_id)
                    osm_vnfs.append(vnf)
                except VnfNotFound:
                    pass

        for osm_vnf in osm_vnfs:
            vnf_instance = {
                "id": osm_vnf["id"],
                "vnfdId": osm_vnf["vnfd-id"],
                "vnfProductName": osm_vnf["vnfd-ref"],
                "vimId": osm_vnf["vim-account-id"],
                # same as the NS
                "instantiationState": osm_ns['_admin']['nsState'],
            }
            if vnf_instance["instantiationState"] == "INSTANTIATED":
                vnf_instance["instantiatedVnfInfo"]["extCpInfo"] = self._cpinfo_converter(osm_vnf)
            sol_ns["vnfInstance"].append(vnf_instance)
        return sol_ns

    @staticmethod
    def _op_im_converter(osm_op):
        sol_op = {
            "id": osm_op["id"],
            "operationState": osm_op["operationState"].upper(),
            "stateEnteredTime": datetime.utcfromtimestamp(osm_op["statusEnteredTime"]).isoformat("T") + "Z",
            "nsInstanceId": osm_op["nsInstanceId"],
            "lcmOperationType": osm_op["lcmOperationType"].upper(),
            "startTime": datetime.utcfromtimestamp(osm_op["startTime"]).isoformat("T") + "Z",
        }
        return sol_op

    @staticmethod
    def _build_url_query(base, args):
        if args and args['args']:
            url_query = urlencode(args['args'])
            return "{0}?{1}".format(base, url_query)
        return base
