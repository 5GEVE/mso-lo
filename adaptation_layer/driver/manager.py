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
from typing import Dict

from .interface import Driver
from .onap import ONAP
from .osm import OSM
from .ever import EVER

_drivers = {}


def get_driver(nfvo_id: int, nfvo_type: str, nfvo_cred: Dict) -> Driver:
    nfvo_type = nfvo_type.casefold()

    global _drivers
    if nfvo_id in _drivers:
        pass
    elif nfvo_type == 'osm':
        _drivers[nfvo_id] = OSM(nfvo_cred)
    elif nfvo_type == 'onap':
        _drivers[nfvo_id] = ONAP(nfvo_cred)
    elif nfvo_type == 'cloudify':
        _drivers[nfvo_id] = EVER(nfvo_cred)
    else:
        raise NotImplementedError(
            'Driver type: {} is not implemented'.format(nfvo_type))
    return _drivers[nfvo_id]
