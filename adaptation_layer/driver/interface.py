from abc import ABC, abstractmethod


class Driver(ABC):

    """
    methods related to Network Service Descriptor
    """
    @abstractmethod
    def get_nsd_list(args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def onboard_nsd(args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_nsd(nsd_info_id: str, args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def update_nsd(nsd_info_id: str, args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def delete_nsd(nsd_info_id: str, args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Virtual Network Function Descriptor
    """
    @abstractmethod
    def get_vnfd_list(args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_vnfd(vnfd_id: str, args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Physical Network Function Descriptor
    """
    @abstractmethod
    def get_pnfd_list(args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_pnfd(pnfd_id: str, args=None) -> dict:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Virtual Network Function
    """
    @abstractmethod
    def get_vnf_list(args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_vnf(vnfId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    """
    methods related to Network Service Descriptor
    """
    @abstractmethod
    def get_ns_list(args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def create_ns(args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def get_ns(nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def instantiate_ns(nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def terminate_ns(nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def scale_ns(nsId: str, args=None) -> list:
        raise NotImplementedError("The method is not implemented")
