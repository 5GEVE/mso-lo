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
    TooManyRedirects, URLRequired, HTTPError, post, put, delete

from error_handler import ServerError, NfvoNotFound, NfvoCredentialsNotFound, \
    Unauthorized, BadRequest, SubscriptionNotFound

logger = logging.getLogger('app.iwf_repository')
IWFREPO_HTTPS = os.getenv('IWFREPO_HTTPS', 'false').lower()
IWFREPO_HOST = os.getenv('IWFREPO_HOST')
IWFREPO_PORT = os.getenv('IWFREPO_PORT')
IWFREPO_INTERVAL = os.getenv('IWFREPO_INTERVAL')

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
    vim_found = get(
        url + '/vimAccounts/search/findByVimAccountNfvoId',
        params={'uuid': osm_vim['_id']})
    vim_found.raise_for_status()
    if vim_found.json()['_embedded']['vimAccounts']:
        logger.info('vim {} found in iwf repository, skip'.format(
            osm_vim['_id']
        ))
    else:
        payload = {
            'vimAccountNfvoId': osm_vim['_id'],
            'name': osm_vim['name'],
            'type': osm_vim['vim_type'],
            'uri': osm_vim['vim_url'],
            'tenant': osm_vim['vim_tenant_name'],
        }
        new_vim = post(url + '/vimAccounts', json=payload)
        new_vim.raise_for_status()
        logger.info('created new vimAccount with id {0}'.format(
            new_vim.json()['vimAccountNfvoId']))
        put(new_vim.json()['_links']['nfvOrchestrators']['href'],
            data=nfvo_self,
            headers={'Content-Type': 'text/uri-list'}).raise_for_status()
        logger.info('associated vimAccount to {0}'.format(nfvo_self))


@_server_error
def find_nfvos_by_type(nfvo_type: str):
    response = get(
        url + '/nfvOrchestrators/search/findByTypeIgnoreCase',
        params={'type': nfvo_type})
    response.raise_for_status()
    return response.json()['_embedded']['nfvOrchestrators']


@_server_error
def _get_nfvo(nfvo_id) -> Dict:
    try:
        resp = get(url + '/nfvOrchestrators/' + nfvo_id)
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
def _convert_nfvo(nfvo: Dict) -> Dict:
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


def convert_cred(nfvo):
    del nfvo['credentials']['id']
    nfvo['credentials']['nfvo_id'] = nfvo['id']
    nfvo['credentials']['user'] = nfvo['credentials'].pop('username')
    return nfvo['credentials']


def get_nfvo_by_id(nfvo_id: int) -> Dict:
    nfvo = _get_nfvo(nfvo_id)
    return _convert_nfvo(nfvo)


def get_nfvo_cred(nfvo_id: int) -> Dict:
    nfvo = _get_nfvo(nfvo_id)
    if nfvo['credentials'] is None:
        raise NfvoCredentialsNotFound(nfvo_id)
    else:
        return convert_cred(nfvo)


@_server_error
def get_nfvo_list() -> List[Dict]:
    try:
        resp = get(url + '/nfvOrchestrators')
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 401:
            raise Unauthorized()
        else:
            raise
    return [_convert_nfvo(nfvo) for nfvo in
            resp.json()['_embedded']['nfvOrchestrators']]


@_server_error
def get_subscription_list(nfvo_id: int) -> Dict:
    try:
        resp = get('{0}/nfvOrchestrators/{1}/subscriptions'.format(url,
                                                                   nfvo_id))
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 401:
            raise Unauthorized()
        else:
            raise
    return resp.json()


@_server_error
def create_subscription(nfvo_id: int, body: Dict):
    try:
        create = post('{0}/subscriptions'.format(url), json=body)
        create.raise_for_status()
        associate = put(create.json()['_links']['nfvOrchestrators']['href'],
                        data='{0}/nfvOrchestrators/{1}'.format(url,
                                                               nfvo_id),
                        headers={'Content-Type': 'text/uri-list'})
        associate.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 400:
            raise BadRequest(description=e.response.text)
        else:
            raise
    return create.json()


@_server_error
def get_subscription(nfvo_id: int, subscriptionId: int) -> Dict:
    try:
        resp = get(
            '{0}/nfvOrchestrators/{1}/subscriptions/{2}'.format(url,
                                                                nfvo_id,
                                                                subscriptionId))
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
        resp = delete(
            '{0}/subscriptions/{1}'.format(url, subscriptionId))
        resp.raise_for_status()
    except HTTPError as e:
        if e.response.status_code == 404:
            raise SubscriptionNotFound(sub_id=subscriptionId)
        else:
            raise


@_server_error
def search_subs_by_ns_instance(ns_instance_id: str) -> List[Dict]:
    try:
        subs = get(url + '/subscriptions/search/findByNsInstanceId',
                   params={'nsInstanceId': ns_instance_id})
        subs.raise_for_status()
    except HTTPError:
        raise
    return subs.json()['_embedded']['subscriptions'] if subs else []
