from abc import ABC, abstractmethod
from typing import List, Dict


class Driver(ABC):
    """
    methods related to Virtual Network Function
    """

    @abstractmethod
    def get_vnf_list(args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_vnf(vnfId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Network Service Descriptor
    """

    @abstractmethod
    def get_ns_list(self, args: Dict = None) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def create_ns(self, args: Dict = None) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def instantiate_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def terminate_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def scale_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")
