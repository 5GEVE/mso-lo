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
import os
from functools import wraps
from typing import List, Dict

from requests import get, ConnectionError, Timeout, \
    TooManyRedirects, URLRequired, HTTPError, post, put, delete, patch

from adaptation_layer.error_handler import ServerError, NfvoNotFound, \
    NfvoCredentialsNotFound, Unauthorized, BadRequest, \
    SubscriptionNotFound, Unprocessable, RanoNotFound, RanoCredentialsNotFound

logger = logging.getLogger('app.iwf_repository')
IWFREPO_HTTPS = os.getenv('IWFREPO_HTTPS', 'false').lower()
IWFREPO_HOST = os.getenv('IWFREPO_HOST')
IWFREPO_PORT = os.getenv('IWFREPO_PORT')
IWFREPO_INTERVAL = os.getenv('IWFREPO_INTERVAL')
accept_h = {'Accept': 'application/hal+json'}
texturi_h = {'Content-Type': 'text/uri-list'}

prot = 'https' if IWFREPO_HTTPS == 'true' else 'http'
host = IWFREPO_HOST if IWFREPO_HOST else 'localhost'
port = int(IWFREPO_PORT) if IWFREPO_PORT else 8087
interval = int(IWFREPO_INTERVAL) if IWFREPO_INTERVAL else 300
url = '{0}://{1}:{2}'.format(prot, host, port)


def _server_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConnectionError, Timeout, TooManyRedirects, URLRequired) as e:
            raise ServerError('problem contacting iwf repository: ' + str(e))

    return wrapper


@_server_error
def post_vim_safe(osm_vim: Dict, nfvo_self: str):
    vim_found = get(f'{url}/vimAccounts/search/findByVimAccountNfvoId', params={'uuid': osm_vim['_id']},
                    headers=accept_h)
    vim_found.raise_for_status()
    if vim_found.json()['_embedded']['vimAccounts']:
        logger.info('vim {} found in iwf repository, skip'.format(osm_vim['_id']))
    else:
        payload = {
            'vimAccountNfvoId': osm_vim['_id'],
            'name': osm_vim['name'],
            'type': osm_vim['vim_type'],
            'uri': osm_vim['vim_url'],
            'tenant': osm_vim['vim_tenant_name'],
        }
        new_vim = post(f'{url}/vimAccounts', json=payload, headers=accept_h)
        new_vim.raise_for_status()
        logger.info('created new vimAccount with id {0}'.format(new_vim.json()['vimAccountNfvoId']))
        put(new_vim.json()['_links']['nfvOrchestrators']['href'], data=nfvo_self,
            headers={**texturi_h, **accept_h}).raise_for_status()
        logger.info('associated vimAccount to {0}'.format(nfvo_self))


@_server_error
def find_nfvos_by_type(nfvo_type: str):
    response = get(f'{url}/nfvOrchestrators/search/findByTypeIgnoreCase', params={'type': nfvo_type}, headers=accept_h)
    response.raise_for_status()
    return response.json()['_embedded']['nfvOrchestrators']


@_server_error
def _get_nfvo(nfvo_id) -> Dict:
    try:
        resp = get(f'{url}/nfvOrchestrators/{nfvo_id}', headers=accept_h)
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 404:
            raise NfvoNotFound(nfvo_id)
        elif e.response.status_code == 401:
            raise Unauthorized()
        else:
            raise
    return resp.json()


@_server_error
def _get_rano(rano_id) -> Dict:
    try:
        resp = get(f'{url}/ranOrchestrators/{rano_id}', headers=accept_h)
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 404:
            raise RanoNotFound(rano_id)
        elif e.response.status_code == 401:
            raise Unauthorized()
        else:
            raise
    return resp.json()


@_server_error
def _convert_nfvo(nfvo: Dict) -> Dict:
    try:
        resp = get(nfvo['_links']['site']['href'], headers=accept_h)
        resp.raise_for_status()
        site = resp.json()['name']
    except HTTPError:
        site = None
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


@_server_error
def _convert_rano(rano: Dict) -> Dict:
    try:
        resp = get(rano['_links']['site']['href'], headers=accept_h)
        resp.raise_for_status()
        site = resp.json()['name']
    except HTTPError:
        site = None
    conv = {
        'id': rano['id'],
        'name': rano['name'],
        'type': rano['type'],
        'site': site
    }
    if rano['uri'] is not None:
        conv['uri'] = rano['uri']
    return conv


def convert_nfvo_cred(orc):
    del orc['credentials']['id']
    orc['credentials']['nfvo_id'] = orc['id']
    orc['credentials']['user'] = orc['credentials'].pop('username')
    return orc['credentials']


def convert_rano_cred(orc):
    del orc['credentials']['id']
    orc['credentials']['rano_id'] = orc['id']
    orc['credentials']['user'] = orc['credentials'].pop('username')
    return orc['credentials']


def get_nfvo_by_id(nfvo_id: int) -> Dict:
    nfvo = _get_nfvo(nfvo_id)
    return _convert_nfvo(nfvo)


def get_rano_by_id(rano_id: int) -> Dict:
    rano = _get_rano(rano_id)
    return _convert_rano(rano)


def get_nfvo_cred(nfvo_id: int) -> Dict:
    nfvo = _get_nfvo(nfvo_id)
    if nfvo['credentials'] is None:
        raise NfvoCredentialsNotFound(nfvo_id)
    else:
        return convert_nfvo_cred(nfvo)


def get_rano_cred(rano_id: int) -> Dict:
    rano = _get_rano(rano_id)
    if rano['credentials'] is None:
        raise RanoCredentialsNotFound(rano_id)
    else:
        return convert_rano_cred(rano)


@_server_error
def get_nfvo_list() -> List[Dict]:
    try:
        resp = get(f'{url}/nfvOrchestrators', headers=accept_h)
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 401:
            raise Unauthorized()
        else:
            raise
    return [_convert_nfvo(nfvo) for nfvo in resp.json()['_embedded']['nfvOrchestrators']]


@_server_error
def get_rano_list() -> List[Dict]:
    try:
        resp = get(f'{url}/ranOrchestrators', headers=accept_h)
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 401:
            raise Unauthorized()
        else:
            raise
    return [_convert_rano(rano) for rano in resp.json()['_embedded']['ranOrchestrators']]


@_server_error
def get_subscription_list(nfvo_id: int) -> Dict:
    try:
        resp = get('{0}/nfvOrchestrators/{1}/subscriptions'.format(url, nfvo_id), headers=accept_h)
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 401:
            raise Unauthorized()
        if e.response.status_code == 404:
            raise NfvoNotFound(nfvo_id)
        else:
            raise
    return resp.json()


@_server_error
def create_subscription(nfvo_id: int, body: Dict):
    try:
        create = post('{0}/subscriptions'.format(url), json=body, headers=accept_h)
        create.raise_for_status()
        associate = put(create.json()['_links']['nfvOrchestrators']['href'],
                        data='{0}/nfvOrchestrators/{1}'.format(url, nfvo_id),
                        headers={**texturi_h, **accept_h})
        associate.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 400:
            raise BadRequest(description=e.response.text)
        if e.response.status_code == 404:
            raise NfvoNotFound(nfvo_id)
        if e.response.status_code == 422:
            raise Unprocessable(description=e.response.text)
        else:
            raise
    return create.json()


@_server_error
def get_subscription(nfvo_id: int, subscriptionId: int) -> Dict:
    try:
        resp = get('{0}/nfvOrchestrators/{1}/subscriptions/{2}'.format(url, nfvo_id, subscriptionId),
                   headers=accept_h)
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 404:
            raise SubscriptionNotFound(sub_id=subscriptionId)
        else:
            raise
    return resp.json()


@_server_error
def delete_subscription(subscriptionId: int) -> None:
    try:
        resp = delete('{0}/subscriptions/{1}'.format(url, subscriptionId))
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 404:
            raise SubscriptionNotFound(sub_id=subscriptionId)
        else:
            raise


@_server_error
def search_subs_by_ns_instance(ns_instance_id: str) -> List[Dict]:
    try:
        subs = get(f'{url}/subscriptions/search/findByNsInstanceId', params={'nsInstanceId': ns_instance_id},
                   headers=accept_h)
        subs.raise_for_status()
    except HTTPError:
        raise
    return subs.json()['_embedded']['subscriptions'] if subs else []


def add_orc_cred_test(orc_type: str, orc_id: int):
    payload = {
        "credentials": {
            "host": "192.168.1.2",
            "port": 9999,
            "username": "admin",
            "password": "admin",
            "project": "admin"
        }
    }
    if orc_type == 'nfvo':
        resp = patch(f'{url}/nfvOrchestrators/{orc_id}', json=payload, headers=accept_h)
    if orc_type == 'rano':
        resp = patch(f'{url}/ranOrchestrators/{orc_id}', json=payload, headers=accept_h)
    resp.raise_for_status()
