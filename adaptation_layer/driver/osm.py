from .interface import Driver


class OSM(Driver):

    @staticmethod
    def get_nsd_list(nfvo_id) -> dict:
        return {'NSDs': ['osm_nsd_1', 'osm_nsd_2']}

    @staticmethod
    def get_nsd(nfvo_id, nsd_id) -> dict:
        return {'NSD': {'id': 'osm_nsd_1'}}
