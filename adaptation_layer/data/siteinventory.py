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
from typing import List, Dict

from requests import Response, get, ConnectionError, Timeout, \
    TooManyRedirects, URLRequired, HTTPError

from error_handler import ServerError, NfvoNotFound, NfvoCredentialsNotFound


class SiteInventory:
    def __init__(self, host: str = 'localhost', port: int = 8087):
        # TODO configuration for site inventory?? where to put it?
        self.host = host
        self.port = port
        # TODO post vim accounts for OSM driver

    @property
    def url(self):
        return 'http://{0}:{1}'.format(self.host, self.port)

    @staticmethod
    def _exec_get(url=None, params=None, headers=None) -> Response:
        try:
            resp = get(url, params=params, headers=headers,
                       verify=False, stream=True)
            resp.raise_for_status()
        except (ConnectionError, Timeout, TooManyRedirects, URLRequired) as e:
            raise ServerError("Problem contacting site inventory: " + str(e))
        return resp

    def _get_nfvo(self, nfvo_id) -> Dict:
        try:
            json = self._exec_get(
                self.url + "/nfvOrchestrators/" + nfvo_id).json()
        except HTTPError as e:
            if e.response.status_code == 404:
                raise NfvoNotFound(nfvo_id)
            else:
                raise ServerError()
        return json

    def get_nfvo_by_id(self, nfvo_id) -> Dict:
        json = self._get_nfvo(nfvo_id)
        return {
            'id': json['id'],
            'name': json['name'],
            'type': json['type'],
        }

    def get_nfvo_cred(self, nfvo_id) -> Dict:
        json = self._get_nfvo(nfvo_id)
        if json['credentials'] is None:
            raise NfvoCredentialsNotFound(nfvo_id)
        else:
            return json['credentials']

    def get_nfvo_list(self) -> List[Dict]:
        json = self._exec_get(self.url + "/nfvOrchestrators").json()
        nfvo_list = []
        for nfvo in json['_embedded']['nfvOrchestrators']:
            nfvo_list.append({
                'id': nfvo['id'],
                'name': nfvo['name'],
                'type': nfvo['type'],
            })
        return nfvo_list
