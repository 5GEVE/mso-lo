from .interface import Driver


class ONAP(Driver):

    @staticmethod
    def get_nsd_list(nfvo_id) -> dict:
        return {'NSDs': ['onap_nsd_1', 'onap_nsd_2']}

    @staticmethod
    def get_nsd(nfvo_id, nsd_id) -> dict:
        return {'NSD': {'id': 'onap_nsd_1'}}
