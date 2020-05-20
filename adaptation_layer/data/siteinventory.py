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
import logging
from functools import wraps
from typing import List, Dict

from requests import get, ConnectionError, Timeout, \
    TooManyRedirects, URLRequired, HTTPError, post, put

from driver.osm import OSM
from error_handler import ServerError, NfvoNotFound, NfvoCredentialsNotFound, \
    Unauthorized, Error

logger = logging.getLogger('app.siteinventory')


def _server_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (ConnectionError, Timeout, TooManyRedirects, URLRequired) as e:
            raise ServerError('Problem contacting site inventory: ' + str(e))

    return wrapper


class SiteInventory:
    def __init__(self, host: str = 'localhost', port: int = 8087):
        # TODO configuration for site inventory?? where to put it?
        self.host = host
        self.port = port
        try:
            self._post_osm_vims()
        except HTTPError as e:
            logger.warning('Cannot add OSM vimAccounts to site inventory')
            logger.warning(e.args[0])

    @property
    def url(self):
        return 'http://{0}:{1}/'.format(self.host, self.port)

    @_server_error
    def _post_vim_safe(self, osm_vim: Dict, nfvo_self: str):
        vim_found = get(
            self.url + 'vimAccounts/search/findByVimAccountNfvoId',
            params={'uuid': osm_vim['_id']})
        vim_found.raise_for_status()
        if not vim_found.json()['_embedded']['vimAccounts']:
            payload = {
                'vimAccountNfvoId': osm_vim['_id'],
                'name': osm_vim['name'],
                'type': osm_vim['vim_type'],
                'uri': osm_vim['vim_url'],
                'tenant': osm_vim['vim_tenant_name'],
            }
            new_vim = post(self.url + 'vimAccounts', json=payload)
            new_vim.raise_for_status()
            logger.info('created new vimAccount with id {0}'.format(
                new_vim.json()['vimAccountNfvoId']))
            put(new_vim.json()['_links']['nfvOrchestrators']['href'],
                data=nfvo_self,
                headers={'Content-Type': 'text/uri-list'}).raise_for_status()
            logger.info('associated vimAccount to {0}'.format(nfvo_self))

    @_server_error
    def _post_osm_vims(self):
        osm_list = get(
            self.url + 'nfvOrchestrators/search/findByTypeIgnoreCase',
            params={'type': 'osm'})
        osm_list.raise_for_status()
        for osm in osm_list.json()['_embedded']['nfvOrchestrators']:
            if osm['credentials'] is not None:
                try:
                    driver = OSM(self._convert_cred(osm))
                    osm_vims, headers = driver.get_vim_list()
                except Error as e:
                    logger.warning(
                        'error contacting osm {0}:{1}'.format(
                            osm['credentials']['host'],
                            osm['credentials']['port'],
                        ))
                    logger.warning(e)
                    continue
                for osm_vim in osm_vims:
                    self._post_vim_safe(osm_vim,
                                        osm['_links']['self']['href'])

    @_server_error
    def _get_nfvo(self, nfvo_id) -> Dict:
        try:
            resp = get(self.url + 'nfvOrchestrators/' + nfvo_id)
            resp.raise_for_status()
            nfvo = resp.json()
        except HTTPError as e:
            if e.response.status_code == 404:
                raise NfvoNotFound(nfvo_id)
            elif e.response.status_code == 401:
                raise Unauthorized()
            else:
                raise
        return nfvo

    @_server_error
    def _convert_nfvo(self, nfvo: Dict) -> Dict:
        site = get(nfvo['_links']['site']['href']).json()['name']
        conv = {
            'id': nfvo['id'],
            'name': nfvo['name'],
            'type': nfvo['type'],
            'site': site
        }
        if nfvo['uri'] is not None:
            conv['uri'] = nfvo['uri']
        if nfvo['createdAt'] is not None:
            conv['createdAt'] = nfvo['createdAt']
        if nfvo['updatedAt'] is not None:
            conv['updatedAt'] = nfvo['updatedAt']
        return conv

    @staticmethod
    def _convert_cred(nfvo):
        del nfvo['credentials']['id']
        nfvo['credentials']['nfvo_id'] = nfvo['id']
        nfvo['credentials']['user'] = nfvo['credentials'].pop('username')
        return nfvo['credentials']

    def get_nfvo_by_id(self, nfvo_id) -> Dict:
        nfvo = self._get_nfvo(nfvo_id)
        return self._convert_nfvo(nfvo)

    def get_nfvo_cred(self, nfvo_id) -> Dict:
        nfvo = self._get_nfvo(nfvo_id)
        if nfvo['credentials'] is None:
            raise NfvoCredentialsNotFound(nfvo_id)
        else:
            return self._convert_cred(nfvo)

    @_server_error
    def get_nfvo_list(self) -> List[Dict]:
        try:
            resp = get(self.url + 'nfvOrchestrators')
            resp.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 401:
                raise Unauthorized()
            else:
                raise
        return [self._convert_nfvo(nfvo) for nfvo in
                resp.json()['_embedded']['nfvOrchestrators']]
