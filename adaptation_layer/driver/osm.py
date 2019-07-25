from .interface import Driver
from osmclient.sol005.client import Client as Osmclient
# from osmclient.common.exceptions import ClientException


class OSM(Driver):

    @staticmethod
    def get_nsd_list(nfvo_id, args) -> dict:
        client = Osmclient(**args)
        return client.nsd.list()

    @staticmethod
    def get_nsd(nfvo_id, nsd_id, args) -> dict:
        client = Osmclient(**args)
        return client.nsd.get(nsd_id)

    @staticmethod
    def onboard_nsd(nfvo_id, args) -> dict:
        client = Osmclient(**args)
        # need to store the yaml/json descriptor in a temporary directory
        # retrive the full path name and pass it to the Osmclient 
        filename = ''
        return client.nsd.create(filename)

    @staticmethod
    def update_nsd(nfvo_id, nsd_info_id: str, args) -> dict:
        client = Osmclient(**args)
        endpoint = '{}/{}/nsd_content'.format(client._apiBase, nsd_info_id)
        # need to store the yaml/json descriptor in a temporary directory
        # retrive the full path name and pass it to the Osmclient 
        filename = ''
        return client.nsd.create(filename, update_endpoint=endpoint)

    @staticmethod
    def delete_nsd(nfvo_id, nsd_info_id: str, args) -> dict:
        client = Osmclient(**args)
        return client.nsd.delete(nsd_info_id)

    @staticmethod
    def get_vnfd_list(nfvo_id: str, args) -> dict:
        client = Osmclient(**args)
        return client.vnfd.list("type=vnfd")

    @staticmethod
    def get_vnfd(nfvo_id, vnfd_id: str, args) -> dict:
        client = Osmclient(**args)
        return client.vnfd.get(vnfd_id)

    @staticmethod
    def get_pnfd_list(nfvo_id: str, args) -> dict:
        client = Osmclient(**args)
        return client.vnfd.list("type=pnfd")

    @staticmethod
    def get_pnfd(nfvo_id, pnfd_id: str, args) -> dict:
        client = Osmclient(**args)
        return client.vnfd.get(pnfd_id)

    @staticmethod
    def get_vnf_list(nfvo_id: str, args) -> list:
        client = Osmclient(**args)
        return client.vnf.list()

    @staticmethod
    def get_vnf(nfvo_id: str, vnfId: str, args) -> list:
        client = Osmclient(**args)
        return client.vnfd.get(vnfId)

    @staticmethod
    def get_ns_list(nfvo_id: str, args) -> list:
        client = Osmclient(**args)
        return client.ns.list()

    @staticmethod
    def create_ns(nfvo_id: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    def get_ns(nfvo_id: str, nsId: str, args) -> list:
        client = Osmclient(**args)
        return client.ns.get(nsId)

    @staticmethod
    def instantiate_ns(nfvo_id: str, nsId: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    def terminate_ns(nfvo_id: str, nsId: str, args) -> list:
        client = Osmclient(**args)
        return client.ns.delete(nsId)

    @staticmethod
    def scale_ns(nfvo_id: str, nsId: str, args) -> list:
        raise NotImplementedError("The method is not implemented")