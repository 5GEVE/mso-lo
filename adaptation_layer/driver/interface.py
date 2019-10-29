from abc import ABC, abstractmethod
from typing import List, Dict


class Driver(ABC):
    """
    methods related to Network Service Descriptor
    """

    @abstractmethod
    def get_ns_list(self, args: Dict = None) -> List[Dict]:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def create_ns(self, args: Dict = None) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_ns(self, nsId: str, args: Dict = None) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def instantiate_ns(self, nsId: str, args: Dict = None) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def terminate_ns(self, nsId: str, args: Dict = None) -> Dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def scale_ns(self, nsId: str, args: Dict = None) -> Dict:
        raise NotImplementedError("The method is not implemented")
