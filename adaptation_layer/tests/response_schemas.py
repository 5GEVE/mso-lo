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
import os

from prance import ResolvingParser

OPENAPI_PATH = os.environ.get("OPENAPI_PATH",
                              '../../openapi/MSO-LO-swagger-resolved.yaml')

openapi = ResolvingParser(OPENAPI_PATH).specification

nfvo_schema = openapi["definitions"]["NFVO"]
nfvo_list_schema = {
    "type": "array",
    "items": nfvo_schema
}

id_schema = openapi["definitions"]["Identifier"]

ns_schema = openapi["definitions"]["NsInstance"]

ns_list_schema = {
    "type": "array",
    "items": ns_schema
}

ns_lcm_op_occ_schema = openapi["definitions"]["NsLcmOpOcc"]

ns_lcm_op_occ_list_schema = {
    "type": "array",
    "items": ns_lcm_op_occ_schema
}

subscription_schema = openapi["definitions"]["LccnSubscription"]
subscription_list_schema = openapi["definitions"][
    "CollectionModel«LccnSubscription»"]
