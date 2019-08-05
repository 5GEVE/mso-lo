from .interface import Driver


class ONAP(Driver):

    @classmethod
    def get_nsd_list(self, args) -> dict:
        return {'NSDs': ['onap_nsd_1', 'onap_nsd_2']}

    @classmethod
    def get_nsd(self, nsd_id: str, args) -> dict:
        return {'NSD': {'id': 'onap_nsd_1'}}
