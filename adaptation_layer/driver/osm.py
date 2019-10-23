from .interface import Driver
from client.osm import Client as Osmclient
from typing import Union

class OSM(Driver):

    def __init__(self, nfvo_auth):
        self._nfvo_auth = nfvo_auth
        self._client = Osmclient(**self._nfvo_auth)

    def get_vnf_list(self, args=None) -> list:
        return self._client.vnf_list(args=args)

    def get_vnf(self, vnfId: str, args=None) -> list:
        return self._client.vnf_get(vnfId, args=args)

    def get_ns_list(self, args=None) -> list:
        ns_list = self._client.ns_list(args=args)
        return self._ns_im_converter(ns_list)

    def create_ns(self, args=None) -> list:
        return self._client.ns_create(args=args)

    def get_ns(self, nsId: str, args=None) -> list:
        ns = self._client.ns_get(nsId, args=args)
        return self._ns_im_converter(ns)

    def instantiate_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_instantiate(nsId, args=args)

    def terminate_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_terminate(nsId, args=args)

    def scale_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_scale(nsId, args=args)

    def _ns_im_converter(self, ns: Union[list, dict]) -> Union[list, dict]:
        if type(ns) is dict:
            result = {
                "id": ns['id'],
                "nsInstanceName": ns['name'],
                "nsInstanceDescription": ns['description'],
                "nsdId": ns['nsd-id'],
                "nsState": ns['_admin']['nsState']
            }
        elif type(ns) is list:
            result = []
            for ins in ns:
                result.append({
                    "id": ins['id'],
                    "nsInstanceName": ins['name'],
                    "nsInstanceDescription": ins['description'],
                    "nsdId": ins['nsd-id'],
                    "nsState": ins['_admin']['nsState']
                })

        return result
