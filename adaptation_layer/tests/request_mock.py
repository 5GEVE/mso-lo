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

mock_ns_scale_v2 = {
    "scaleType": "SCALE_VNF",
    "scaleVnfData": [{
        "scaleVnfType": "SCALE_IN",
        "scaleByStepData": {
          "aspectId": "1234"
        }
    }]
}
mock_ns_scale = {
    "scaleType": "SCALE_VNF",
    "scaleVnfData": {
        "scaleVnfType": "SCALE_IN",
        "scaleByStepData": {
            "scaling-group-descriptor": "12313"
        }
    }
}

mock_ns = {
    "nsdId": "49ccb6a2-5bcd-4f35-a2cf-7728c54e48b7",
    "nsName": "test",
    "nsDescription": "test description"
}

mock_ns_instantiate = {
  "nsFlavourId": "vDCN_001",
  "nsInstantiationLevelId": "1",
  "additionalParamsForNs": {
    "vld": [
      {
        "name": "vldnet",
        "vim-network-name": "netVIM1"
      }
    ],
    "vnf": [
      {
        "vnfInstanceId": "string",
        "vimAccountId": "string"
      }
    ],
    "wim_account": "WimAccount1"
  }
}

mock_ns_instantiatev2 = {
  "nsFlavourId": "vDCN_001",
  "nsInstantiationLevelId": "1"
}

mock_ns_terminate = {
    "terminationTime": "2017-07-21T17:32:28Z"
}
