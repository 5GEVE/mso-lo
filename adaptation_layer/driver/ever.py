#  Copyright 2020 Ericsson TEI, Fabio Ubaldi
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
import copy
import logging
import os
import re
from typing import Dict, Tuple
from urllib.parse import urlencode

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from adaptation_layer.error_handler import ResourceNotFound, NsNotFound, \
    BadRequest, ServerError, NsOpNotFound, NsdNotFound
from .interface import Driver, Headers, BodyList, Body

urllib3.disable_warnings(InsecureRequestWarning)
TESTING = os.environ.get("TESTING", False)
PRISM_ALIAS = os.environ.get("PRISM_ALIAS", "prism-ever")

logger = logging.getLogger('app.driver.ever')

class EVER(Driver):

    def __init__(self, rano_cred):
        self._ranoId = rano_cred["rano_id"]
        self._host = rano_cred["host"]
        self._port = rano_cred["port"] if "port" in rano_cred else 8080
        self._headers = {"Content-Type": "application/json",
                         "Accept": "application/json"}

        if TESTING is False:
            self._base_path = 'http://{0}:{1}'.format(self._host, self._port)
        else:
            self._base_path = 'http://{0}:{1}'.format(PRISM_ALIAS, 9999)

    def _exec_delete(self, url=None, params=None, headers=None):
        logger.debug('#############execute delete######')
        logger.debug('url= ' + url)
        try:
            resp = requests.delete(url, params=params, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 206):
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), resp.headers
            else:
                return resp.text, resp.headers
        elif resp.status_code == 204:
            return None, resp.headers
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            error = resp.json()
            logger.debug('############')
            logger.debug('error: ' + error)
            logger.debug('###########')
            raise ServerError(error)

    def _exec_post(self, url=None, data=None, json=None, headers=None):
        logger.debug('#############execute post######')
        logger.debug('url= ' + url)
        try:
            resp = requests.post(url, data=data, json=json, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 206):
            try:
                ctype = resp.headers['content-type']
            except KeyError:
                # success but no content
                return None, resp.headers
            if 'application/json' in ctype:
                return resp.json(), resp.headers
            else:
                return resp.text, resp.headers
        elif resp.status_code == 204:
            return None, resp.headers
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            if 'application/json' in resp.headers['content-type']:
                error = resp.json()
            else:
                error = resp.text
            logger.debug('############')
            logger.debug('error: ' + error)
            logger.debug('###########')
            raise ServerError(error)

    def _exec_get(self, url=None, params=None, headers=None):
        logger.debug('#############execute get######')
        logger.debug('url= ' + url)
        try:
            resp = requests.get(url, params=params, verify=False, headers=headers)
        except Exception as e:
            raise ServerError(str(e))

        if resp.status_code in (200, 201, 202, 206):
            if 'application/json' in resp.headers['content-type']:
                return resp.json(), resp.headers
            else:
                return resp.text, resp.headers
        elif resp.status_code == 204:
            return None, resp.headers
        elif resp.status_code == 400:
            raise BadRequest()
        elif resp.status_code == 404:
            raise ResourceNotFound()
        else:
            error = resp.json()
            logger.debug('############')
            logger.debug('error: ' + error)
            logger.debug('###########')
            raise ServerError(error)

    # all methods

    def get_ns_list(self, args=None) -> Tuple[BodyList, Headers]:
        _url = '{0}/instances'.format(self._base_path)
        _url = self._build_url_query(_url, args)
        ns_list, resp_headers = self._exec_get(_url, headers=self._headers)
        headers = self._build_headers(resp_headers)
        return ns_list, headers

    def create_ns(self, args=None) -> Tuple[Body, Headers]:
        _url = '{0}/create'.format(self._base_path)
        _url = self._build_url_query(_url, args)
        try:
            created_ns, resp_headers = self._exec_post(
                _url, json=args['payload'], headers=self._headers)
        except ResourceNotFound:
            nsd_Id = args['payload']['nsdId']
            raise NsdNotFound(nsd_id=nsd_Id)
        headers = self._build_headers(resp_headers)
        return created_ns, headers

    def get_ns(self, nsId: str, args=None, skip_sol=False) -> Tuple[Body, Headers]:
        _url = '{0}/instances/{1}'.format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            ns_instance, resp_headers = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return ns_instance, headers

    def delete_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
        _url = '{0}/delete/{1}'.format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        try:
            empty_body, resp_headers = self._exec_delete(
                _url, params=None, headers={})
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return None, headers

    def instantiate_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        _url = '{0}/instantiate/{1}'.format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        instantiate_payload = {}
        try:
            instantiate_payload['SapData'] = args['payload']['SapData']
        except (TypeError, KeyError):
            logger.info('no SapData')
        try:
            empty_body, resp_headers = self._exec_post(
                _url, json=instantiate_payload, headers={})
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return None, headers

    def terminate_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        _url = '{0}/terminate/{1}'.format(self._base_path, nsId)
        _url = self._build_url_query(_url, args)
        req_headers = copy.deepcopy(self._headers)
        try:
            del req_headers["Content-Type"]
        except KeyError:
            pass
        try:
            del req_headers["Accept"]
        except KeyError:
            pass
        try:
            emtpy_body, resp_headers = self._exec_post(_url, headers=req_headers)
        except ResourceNotFound:
            raise NsNotFound(ns_id=nsId)
        headers = self._build_headers(resp_headers)
        return None, headers

    def scale_ns(self, nsId: str, args=None) -> Tuple[None, Headers]:
        pass

    def get_op_list(self, args: Dict = None) -> Tuple[BodyList, Headers]:
        _url = "{0}/ns_lcm_op_occs".format(self._base_path)
        _url = self._build_url_query(_url, args)
        op_list, resp_headers = self._exec_get(_url, headers=self._headers)
        headers = self._build_headers(resp_headers)
        return op_list, headers

    def get_op(self, nsLcmOpId, args: Dict = None) -> Tuple[Body, Headers]:
        _url = '{0}/ns_lcm_op_occs/{1}'.format(self._base_path, nsLcmOpId)
        _url = self._build_url_query(_url, args)
        try:
            lcm_op, resp_headers = self._exec_get(_url, headers=self._headers)
        except ResourceNotFound:
            raise NsOpNotFound(ns_op_id=nsLcmOpId)
        headers = self._build_headers(resp_headers)
        return lcm_op, headers

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
                r"/(instances|ns_lcm_op_occs)/([A-Za-z0-9\-]+)", resp_headers['location'])
            if len(re_res):
                headers['location'] = '/rano/{0}/ns_lcm_op_occs/{1}'.format(self._ranoId, re_res[0][1])
        return headers
