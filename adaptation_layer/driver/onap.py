from typing import Dict, List
from client.onap import Client as ONAPclient
from client.onap import AgentClient as AGENTclient
from .interface import Driver


class ONAP(Driver):

    def __init__(self):
        self._client = ONAPclient()
        self._agent = AGENTclient()
        # self._client = ONAPclient(**self)

    def create_ns(self, args: Dict = None) -> Dict:
        ns_name = self._client.check_ns_name(args['payload']['nsdId'])  # retrieve name of nsdId
        return self._agent.ns_create(ns_name['name'], args=args)

    def get_ns_list(self, args=None) -> List[Dict]:
        return self._agent.ns_list()

    def get_ns(self, nsId: str, args=None) -> Dict:
        return self._agent.ns_get(nsId, args=args)

    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        return self._agent.ns_delete(nsId, args=args)

    def instantiate_ns(self, nsId: str, args: Dict = None) -> None:
        return self._agent.ns_instantiate(nsId, args=args)

    # unsupported by ONAP
    def scale_ns(self, nsId: str, args: Dict = None) -> None:
        pass

    def terminate_ns(self, nsId: str, args: Dict = None) -> None:
        return self._agent.ns_terminate(nsId, args=args)

    def get_op_list(self, args: Dict = None) -> List[Dict]:
        return self._agent.get_op_list()

    def get_op(self, nsLcmOpId: str, args: Dict = None) -> Dict:
        return self._agent.get_op(nsLcmOpId, args=args)

