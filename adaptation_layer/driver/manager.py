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

from database import Database
from .interface import Driver
from .onap import ONAP
from .osm import OSM

_drivers = {}


def get_driver(nfvo_id: int, db: Database) -> Driver:
    global _drivers
    if nfvo_id not in _drivers:
        nfvo = db.get_nfvo_by_id(nfvo_id)
        nfvo_type = nfvo['type'].casefold()
        nfvo_cred = db.get_nfvo_cred(nfvo_id)
        if nfvo_type == 'osm':
            _drivers[nfvo_id] = OSM(nfvo_cred, db)
        elif nfvo_type == 'onap':
            _drivers[nfvo_id] = ONAP(nfvo_cred)
        else:
            raise NotImplementedError(
                'Driver type: {} is not implemented'.format(nfvo_type))
    return _drivers[nfvo_id]
