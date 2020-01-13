from abc import ABC, abstractmethod
from typing import List, Dict, NewType, Tuple


class Driver(ABC):
    """
    methods related to Network Service Descriptor
    """
    Headers = Dict
    Body = Dict
    BodyList = List[Dict]

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
    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def instantiate_ns(self, nsId: str, args: Dict = None) -> None:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def terminate_ns(self, nsId: str, args: Dict = None) -> None:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def scale_ns(self, nsId: str, args: Dict = None) -> None:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_op_list(self, nsId: str, args: Dict = None) -> Tuple[BodyList, Headers]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_op(self, nsLcmOpId, args: Dict = None) -> Tuple[Body, Headers]:
        raise NotImplementedError("The method is not implemented")