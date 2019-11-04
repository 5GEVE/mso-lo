from .interface import Driver
from .osm import OSM
from .onap import ONAP
from error_handler import NfvoNotFound, NsNotFound, Unauthorized, BadRequest
from models import NFVO
from app import db
from flask import jsonify


nfvo_mock_osm = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'project': 'admin'
}


def get_driver(nfvo_id) -> Driver:
    nfvo = NFVO.query.filter_by(id=nfvo_id).first()
    if nfvo is None:
        raise NfvoNotFound(nfvo_id=nfvo_id)
    nfvo = nfvo.serialize
    type = nfvo['type'].casefold()
    if type == 'osm':
        return OSM(nfvo_mock_osm)
    elif type == 'onap':
        return ONAP()
    else:
        raise NotImplementedError(
            'Driver type: {} is not implemented'.format(type))


def get_nfvo_list(args=None) -> list:
    results = NFVO.query.all()
    nfvo_list = [result.serialize for result in results]

    return nfvo_list


def get_nfvo(nfvo_id, args=None) -> dict:
    nfvo = NFVO.query.filter_by(id=nfvo_id).first()
    if nfvo is None:
        raise NfvoNotFound(nfvo_id=nfvo_id)
    return nfvo.serialize
