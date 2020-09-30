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

from .ever import EVER
from .fivegr_so import FIVEGR_SO
from .interface import Driver
from .onap import ONAP
from .osm import OSM


def get_driver(orc_type: str, orc_id: int, db) -> Driver:
    if orc_type == 'nfvo':
        nfvo = db.get_nfvo_by_id(orc_id)
        nfvo_type = nfvo['type'].casefold()
        nfvo_cred = db.get_nfvo_cred(orc_id)
        if nfvo_type == 'osm':
            return OSM(nfvo_cred)
        elif nfvo_type == 'onap':
            return ONAP(nfvo_cred)
        elif nfvo_type == 'ever':
            return EVER(nfvo_cred)
        elif nfvo_type == '5gr-so':
            return FIVEGR_SO(nfvo_cred)
        else:
            raise NotImplementedError(
                'Driver type: {} is not implemented'.format(nfvo_type))
    elif orc_type == 'rano':
        rano = db.get_rano_by_id(orc_id)
        rano_type = rano['type'].casefold()
        rano_cred = db.get_rano_cred(orc_id)
        if rano_type == 'ever':
            return EVER(rano_cred)
        else:
            raise NotImplementedError(
                'Driver type: {} is not implemented'.format(rano_type))
