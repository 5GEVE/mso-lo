from typing import Dict, List
from client.onap import Client as ONAPclient
from .interface import Driver


# Driver = 'onap'

# class ONAP(Driver):
class ONAP(object):

    def __init__(self):
        self._client = ONAPclient()
        # self._client = ONAPclient(**self) - jak to ma byc czy potrzbne odwolanie czy tak jak wyzej wystarczy

    # def create_ns(self, args: Dict = None) -> Dict:
    #     pass

    def get_ns_list(self, args=None) -> List[Dict]:
        ns = self._client.ns_list()
        return self._ns_converter(ns)

    def get_ns(self, nsId: str) -> Dict:
        ns = self._client.ns_get(nsId)
        return self._ns_converter(ns)

    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        pass



    #
    # def instantiate_ns(self, nsId: str, args: Dict = None) -> None:
    #     pass
    #
    # def scale_ns(self, nsId: str, args: Dict = None) -> None:
    #     pass
    #
    # def terminate_ns(self, nsId: str, args: Dict = None) -> None:
    #     pass

    def _ns_converter(self, ns):

        if type(ns) is dict:
            result = {
                "id": ns["id"],
                "nsInstanceName": ns['name'],
                "nsInstanceDescription": 'null',
                "nsdId": ns['serviceSpecification']['id'],
                "nsState": 'INSTANTIATED'
            }

        elif type(ns) is list:
            result = []
            for element in ns:
                result.append({
                    "id": element['id'],
                    "nsInstanceName": element['name'],
                    "nsInstanceDescription": 'null',
                    "nsdId": element['serviceSpecification']['id'],
                    # permited value of nsState: NOT_INSTANTIATED, INSTANTIATED
                    # "nsState": element['distributionStatus']
                    # zalozenie ze wszystjkie dostepne z api serwisy sa instantiated
                    "nsState": 'INSTANTIATED'
                    })

        return result
