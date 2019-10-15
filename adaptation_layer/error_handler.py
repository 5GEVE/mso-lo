from flask import make_response, jsonify


def init_errorhandler(app):
    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({'error': error.description}), 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return make_response(jsonify({'error': error.description}), 401)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': error.description}), 404)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NfvoNotFound(Error):
    def __init__(self, nfvo_id):
        self.description = 'NFVO {0} not found.'.format(nfvo_id)


class NsNotFound(Error):
    def __init__(self, ns_id=None):
        self.description = 'NS instance {0} not found.'.format(ns_id)


class Unauthorized(Error):
    def __init__(self):
        self.description = 'Unauthorized'


class BadRequest(Error):
    def __init__(self, description=None):
        if description is not None:
            self.description = description
        else:
            self.description = 'Malformed request'
