from .interface import Driver
# from osmclient.sol005.client import Client as Osmclient
# from osmclient.common.exceptions import ClientException
from client.osm import Client as Osmclient


class OSM(Driver):

    def __init__(self, nfvo_auth):
        self._nfvo_auth = nfvo_auth
        self._client = Osmclient(**self._nfvo_auth)

    def get_vnf_list(self, args=None) -> list:
        return self._client.vnf_list(args=args)

    def get_vnf(self, vnfId: str, args=None) -> list:
        return self._client.vnf_get(vnfId, args=args)

    def get_ns_list(self, args=None) -> list:
        return self._client.ns_list(args=args)

    def create_ns(self, args=None) -> list:
        return self._client.ns_create(args=args)

    def get_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_get(nsId, args=args)

    def instantiate_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_instantiate(nsId, args=args)

    def terminate_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_terminate(nsId, args=args)

    def scale_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_scale(nsId, args=args)
