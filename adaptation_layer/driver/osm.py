from .interface import Driver
from osmclient.sol005.client import Client as Osmclient
# from osmclient.common.exceptions import ClientException


class OSM(Driver):

    def __init__(self, nfvo_auth):
        self._nfvo_auth = nfvo_auth
        self._client = Osmclient(**self._nfvo_auth)

    def get_nsd_list(self, args=None) -> dict:
        return self._client.nsd.list()

    def get_nsd(self, nsd_id: str) -> dict:
        return self._client.nsd.get(nsd_id)

    def onboard_nsd(self, args=None) -> dict:
        # need to store the yaml/json descriptor in a temporary directory
        # retrive the full path name and pass it to the Osmclient
        filename = ''
        return self._client.nsd.create(filename)

    def update_nsd(self, nsd_info_id: str, args=None) -> dict:
        endpoint = '{}/{}/nsd_content'.format(
            self._client._apiBase,
            nsd_info_id)
        # need to store the yaml/json descriptor in a temporary directory
        # retrive the full path name and pass it to the Osmclient
        filename = ''
        return self._client.nsd.create(filename, update_endpoint=endpoint)

    def delete_nsd(self, nsd_info_id: str, args=None) -> dict:
        return self._client.nsd.delete(nsd_info_id)

    def get_vnfd_list(self, args=None) -> dict:
        return self._client.vnfd.list("type=vnfd")

    def get_vnfd(self, vnfd_id: str, args=None) -> dict:
        return self._client.vnfd.get(vnfd_id)

    def get_pnfd_list(self, args=None) -> dict:
        return self._client.vnfd.list("type=pnfd")

    def get_pnfd(self, pnfd_id: str, args=None) -> dict:
        return self._client.vnfd.get(pnfd_id)

    def get_vnf_list(self, args=None) -> list:
        return self._client.vnf.list()

    def get_vnf(self, vnfId: str, args=None) -> list:
        return self._client.vnfd.get(vnfId)

    def get_ns_list(self, args=None) -> list:
        return self._client.ns.list()

    def create_ns(self, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    def get_ns(self, nsId: str, args=None) -> list:
        return self._client.ns.get(nsId)

    def instantiate_ns(self, nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    def terminate_ns(self, nsId: str, args=None) -> list:
        return self._client.ns.delete(nsId)

    def scale_ns(self, nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")
