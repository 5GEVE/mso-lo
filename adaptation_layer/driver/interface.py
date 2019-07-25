from abc import ABC, abstractmethod


class Driver(ABC):

    """
    methods related to Network Service Descriptor
    """
    @staticmethod
    @abstractmethod
    def get_nsd_list(nfvo_id: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def onboard_nsd(nfvo_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def get_nsd(nfvo_id, nsd_info_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def update_nsd(nfvo_id, nsd_info_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def delete_nsd(nfvo_id, nsd_info_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Virtual Network Function Descriptor
    """
    @staticmethod
    @abstractmethod
    def get_vnfd_list(nfvo_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def get_vnfd(nfvo_id, vnfd_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Physical Network Function Descriptor
    """
    @staticmethod
    @abstractmethod
    def get_pnfd_list(nfvo_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def get_pnfd(nfvo_id, pnfd_id: str, args) -> dict:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Virtual Network Function
    """
    @staticmethod
    @abstractmethod
    def get_vnf_list(nfvo_id: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def get_vnf(nfvo_id: str, vnfId: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Network Service Descriptor
    """
    @staticmethod
    @abstractmethod
    def get_ns_list(nfvo_id: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def create_ns(nfvo_id: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def get_ns(nfvo_id: str, nsId: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def instantiate_ns(nfvo_id: str, nsId: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def terminate_ns(nfvo_id: str, nsId: str, args) -> list:
        raise NotImplementedError("The method is not implemented")

    @staticmethod
    @abstractmethod
    def scale_ns(nfvo_id: str, nsId: str, args) -> list:
        raise NotImplementedError("The method is not implemented")
