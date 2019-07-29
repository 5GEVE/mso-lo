from .interface import Driver
from .osm import OSM
from .onap import ONAP

# mock nvfo list
nfvo_list = [
    {
        "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
        "name": "OSM-Turin",
        "nfvoType": "OSM",
        "location": "Italy",
        "uri": "https://osm-turin.5g-eve.eu",
        "createdAt": "2019-06-29T09:12:33.001Z",
        "updatedAt": "2019-06-29T09:12:33.001Z"
    }
]

nfvo_mock_osm = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'project': 'admin'
}


def get_driver(nfvo_id) -> Driver:
    # checks the nfvo_id against the database and gets the type
    type = 'osm'

    if type == 'osm':
        return OSM(nfvo_mock_osm)
    elif type == 'onap':
        return ONAP()
    else:
        raise NotImplementedError(
            'Driver type: {} is not implemented'.format(type))


def get_nfvo_list() -> list:
    # return a mock list
    return nfvo_list


def get_nfvo(nfvo_id) -> dict:
    # return a mock nvfo data
    return nfvo_list[0]
