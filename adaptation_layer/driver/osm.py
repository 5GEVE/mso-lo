from .interface import Driver
# from osmclient.sol005.client import Client as Osmclient
# from osmclient.common.exceptions import ClientException
from client.osm import Client as Osmclient


class OSM(Driver):

    def __init__(self, nfvo_auth):
        self._nfvo_auth = nfvo_auth
        self._client = Osmclient(**self._nfvo_auth)

    def get_vnf_list(self, args=None) -> list:
        return self._client.vnf_list()

    def get_vnf(self, vnfId: str, args=None) -> list:
        return self._client.vnf_get(vnfId)

    def get_ns_list(self, args=None) -> list:
        return self._client.ns_list()

    def create_ns(self, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    def get_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_get(nsId)

    def instantiate_ns(self, nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    def terminate_ns(self, nsId: str, args=None) -> list:
        return self._client.ns_delete(nsId)

    def scale_ns(self, nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")
