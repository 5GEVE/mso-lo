from .interface import Driver
from .osm import OSM
from .onap import ONAP


def get_driver(nfvo_id) -> Driver:
    # checks the nfvo_id against the database and gets the type
    type = 'osm'

    if type == 'osm':
        return OSM()
    elif type == 'onap':
        return ONAP()
    else:
        raise NotImplementedError('Driver type: {} is not implemented'.format(type))
