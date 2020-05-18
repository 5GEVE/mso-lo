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

import requests

# TODO configuration for site inventory?? where to put it?
from error_handler import ServerError

host = "http://localhost:8087"


def _exec_get(url=None, params=None, headers=None):
    try:
        resp = requests.get(url, params=params,
                            verify=False, stream=True, headers=headers)
    except Exception as e:
        raise ServerError("Problem contacting site-inventory: " + str(e))
    return resp


def get_nfvo_by_id(nfvo_id) -> Dict:
    json = _exec_get(host + "/nfvOrchestrators/" + nfvo_id).json()
    return {
        'id': json['id'],
        'name': json['name'],
        'type': json['type'],
    }


def get_nfvo_list() -> List[Dict]:
    json = _exec_get(host + "/nfvOrchestrators").json()
    nfvo_list = []
    for nfvo in json['_embedded']['nfvOrchestrators']:
        nfvo_list.append({
            'id': nfvo['id'],
            'name': nfvo['name'],
            'type': nfvo['type'],
        })
    return nfvo_list


def get_nfvo_cred(nfvo_id) -> Dict:
    pass
