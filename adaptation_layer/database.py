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
from abc import ABC, abstractmethod
from typing import Dict, List


class Database(ABC):

    @abstractmethod
    def get_nfvo_by_id(self, nfvo_id: int) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_nfvo_cred(self, nfvo_id: int) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_nfvo_list(self) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_subscription_list(self, nfvo_id: int) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def create_subscription(self, nfvo_id: int, body: Dict) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_subscription(self, nfvo_id: int, subscriptionId: int) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def delete_subscription(self, subscriptionId: int) -> None:
        raise NotImplementedError("The method is not implemented")
