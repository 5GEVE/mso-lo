from typing import Dict, List

from client.osm import Client as Osmclient
from .interface import Driver


class OSM(Driver):

    def __init__(self, nfvo_auth):
        self._nfvo_auth = nfvo_auth
        self._client = Osmclient(**self._nfvo_auth)

    def get_vnf_list(self, args=None) -> list:
        return self._client.vnf_list(args=args)

    def get_vnf(self, vnfId: str, args=None) -> list:
        return self._client.vnf_get(vnfId, args=args)

    def get_ns_list(self, args=None) -> List[Dict]:
        ns_list = self._client.ns_list(args=args)
        return self._ns_list_converter(ns_list)

    def create_ns(self, args=None) -> Dict:
        return self._client.ns_create(args=args)

    def get_ns(self, nsId: str, args=None) -> Dict:
        ns = self._client.ns_get(nsId, args=args)
        return self._ns_im_converter(ns)

    def delete_ns(self, nsId: str, args: Dict = None) -> None:
        return self._client.ns_delete(nsId, args=args)

    def instantiate_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_instantiate(nsId, args=args)

    def terminate_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_terminate(nsId, args=args)

    def scale_ns(self, nsId: str, args=None) -> None:
        return self._client.ns_scale(nsId, args=args)

    def get_op_list(self, args: Dict = None) -> List[Dict]:
        nsId = None
        if args['args'] and len(args['args']) > 0:
            nsId = args['args']['nsInstanceId'] if 'nsInstanceId' in args['args'] else None
        return self._client.ns_op_list(nsId, args=args)

    def get_op(self, nsLcmOpId, args: Dict = None) -> Dict:
        return self._client.ns_op(nsLcmOpId, args=args)

    def _ns_im_converter(self, ns: Dict) -> Dict:
        result = {
            "id": ns['id'],
            "nsInstanceName": ns['name'],
            "nsInstanceDescription": ns['description'],
            "nsdId": ns['nsd-id'],
            "nsState": ns['_admin']['nsState']
        }
        return result

    def _ns_list_converter(self, ns_list: List[Dict]):
        result = []
        for ins in ns_list:
            result.append(self._ns_im_converter(ins))
        return result
