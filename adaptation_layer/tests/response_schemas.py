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

from prance import ResolvingParser

spec = ResolvingParser(
    "../../openapi/MSO-LO-3.3-swagger-resolved.yaml").specification
id_schema = spec["definitions"]["Identifier"]
ns_schema = spec["definitions"]["NsInstance"]
ns_list_schema = {
    "type": "array",
    "items": ns_schema
}
ns_lcm_op_occ_schema = spec["definitions"]["NsLcmOpOcc"]
ns_lcm_op_occ_list_schema = {
    "type": "array",
    "items": ns_lcm_op_occ_schema
}
