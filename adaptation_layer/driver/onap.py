from typing import Dict, List

from .interface import Driver


class ONAP(Driver):

    def create_ns(self, args: Dict = None) -> Dict:
        pass

    def get_ns_list(self, args: Dict = None) -> List[Dict]:
        pass

    def get_ns(self, nsId: str, args: Dict = None) -> Dict:
        pass

    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        pass

    def instantiate_ns(self, nsId: str, args: Dict = None) -> None:
        pass

    def scale_ns(self, nsId: str, args: Dict = None) -> None:
        pass

    def terminate_ns(self, nsId: str, args: Dict = None) -> None:
        pass
