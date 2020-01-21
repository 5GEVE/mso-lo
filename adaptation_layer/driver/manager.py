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

from error_handler import NfvoNotFound
from models import NFVO, NFVO_CREDENTIALS
from .interface import Driver
from .onap import ONAP
from .osm import OSM


def get_driver(nfvo_id) -> Driver:
    nfvo = NFVO.query.filter_by(id=nfvo_id).first()
    nfvo_cred = NFVO_CREDENTIALS.query.filter_by(nfvo_id=nfvo_id).first()
    if nfvo is None or nfvo_cred is None:
        raise NfvoNotFound(nfvo_id=nfvo_id)
    nfvo = nfvo.serialize
    nfvo_cred = nfvo_cred.serialize
    type = nfvo['type'].casefold()
    if type == 'osm':
        return OSM(nfvo_cred)
    elif type == 'onap':
        return ONAP(nfvo_cred)
    else:
        raise NotImplementedError(
            'Driver type: {} is not implemented'.format(type))


def get_nfvo_list(args=None) -> list:
    results = NFVO.query.all()
    nfvo_list = [result.serialize for result in results]

    return nfvo_list


def get_nfvo(nfvo_id, args=None) -> dict:
    nfvo = NFVO.query.filter_by(id=nfvo_id).first()
    if nfvo is None:
        raise NfvoNotFound(nfvo_id=nfvo_id)
    return nfvo.serialize
