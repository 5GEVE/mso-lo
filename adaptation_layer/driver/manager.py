from .interface import Driver
from .osm import OSM
from .onap import ONAP
from error_handler import NfvoNotFound, NsNotFound, Unauthorized, BadRequest
from models import NFVO, NFVO_CREDENTIALS
from app import db
from flask import jsonify


def get_driver(nfvo_id) -> Driver:
    nfvo = NFVO.query.filter_by(id=nfvo_id).first()
    nfvo_cred = NFVO_CREDENTIALS.query.filter_by(nfvo_id=nfvo_id).first()
    if nfvo is None or nfvo_cred is None:
        raise NfvoNotFound(nfvo_id=nfvo_id)
    nfvo = nfvo.serialize
    nfvo_cred = nfvo_cred.serialize
    type = nfvo['type'].casefold()
    if type == 'osm':
        return OSM(nfvo_cred)
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
