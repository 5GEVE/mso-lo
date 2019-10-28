from typing import Dict, List

from .interface import Driver


class ONAP(Driver):

    def get_ns_list(self, args: Dict = None) -> List[Dict]:
        pass

    def create_ns(self, args: Dict = None) -> List[Dict]:
        pass

    def get_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        pass

    def instantiate_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        pass

    def terminate_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        pass

    def scale_ns(self, nsId: str, args: Dict = None) -> List[Dict]:
        pass