from abc import ABC, abstractmethod


class Driver(ABC):

    @staticmethod
    @abstractmethod
    def get_nsd_list(nfvo_id: str) -> dict:
        raise NotImplementedError("The method not implemented")

    @staticmethod
    @abstractmethod
    def get_nsd(nfvo_id, nsd_id) -> dict:
        raise NotImplementedError("The method not implemented")
