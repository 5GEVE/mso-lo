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

id_schema = {"type": "string",
             "pattern": "^[a-fA-F0-9]{8}(-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}$"}

ns_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "nsInstanceName": {"type": "string"},
        "nsInstanceDescription": {"type": "string"},
        "nsdId": {"type": "string"},
        "nsState": {"type": "string"},
        "vnfInstance": {"type": "array"}
    },
    "required": ["id", "nsInstanceName", "nsInstanceDescription", "nsdId", "nsState"],
    "additionalProperties": False
}

ns_list_schema = {
    "type": "array",
    "items": ns_schema
}

ns_lcm_op_occ_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "operationState": {"type": "string"},
        "stateEnteredTime": {"type": "string", "format": "date-time"},
        "nsInstanceId": {"type": "string"},
        "lcmOperationType": {"type": "string"},
        "startTime": {"type": "string", "format": "date-time"}
    }
}

ns_lcm_op_occ_list_schema = {
    "type": "array",
    "items": ns_lcm_op_occ_schema
}
