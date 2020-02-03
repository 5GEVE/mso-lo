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
import fnmatch
import os

from prance import ResolvingParser

file_path = None
openapi_dir = '../../openapi/'
for file in os.listdir(openapi_dir):
    if fnmatch.fnmatch(file, 'MSO-LO-?.?-swagger-resolved.yaml'):
        file_path = os.path.join(openapi_dir, file)
if file_path is None:
    raise FileNotFoundError("Openapi file not found.")

openapi = ResolvingParser(file_path).specification
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
