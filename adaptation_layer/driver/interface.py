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
from typing import List, Dict, Tuple

Headers = Dict
Body = Dict
BodyList = List[Dict]


class Driver(ABC):

    @abstractmethod
    def get_ns_list(self, args: Dict = None) -> Tuple[BodyList, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def create_ns(self, args: Dict = None) -> Tuple[Body, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_ns(self, nsId: str, args: Dict = None) -> Tuple[Body, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def delete_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def instantiate_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def terminate_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def scale_ns(self, nsId: str, args: Dict = None) -> Tuple[None, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_op_list(self, args: Dict = None) -> Tuple[BodyList, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_op(self, nsLcmOpId, args: Dict = None) -> Tuple[Body, Headers]:
        raise NotImplementedError("The method is not implemented")
