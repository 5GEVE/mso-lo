#  Copyright 2019 CNIT, Francesco Lombardo, Matteo Pergolesi
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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

    @app.errorhandler(500)
    def server_error(error):
        return make_response(jsonify({'error': error.description}), 500)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NfvoNotFound(Error):
    def __init__(self, nfvo_id):
        self.description = 'NFVO {0} not found.'.format(nfvo_id)


class ResourceNotFound(Error):
    def __init__(self):
        self.description = 'Resource not found.'

class VimNotFound(Error):
    def __init__(self):
        self.description = 'Resource not found.'


class NsOpNotFound(Error):
    def __init__(self, ns_op_id=None):
        self.description = 'NS LCM operatione {0} not found.'.format(ns_op_id)


class NsNotFound(Error):
    def __init__(self, ns_id=None):
        self.description = 'NS instance {0} not found.'.format(ns_id)


class VnfNotFound(Error):
    def __init__(self, vnf_id=None):
        self.description = 'VNF instance {0} not found.'.format(vnf_id)


class VnfPkgNotFound(Error):
    def __init__(self, vnfpkg_id=None):
        self.description = 'VNF package {0} not found.'.format(vnfpkg_id)


class Unauthorized(Error):
    def __init__(self):
        self.description = 'Unauthorized'


class BadRequest(Error):
    def __init__(self, description=None):
        if description is not None:
            self.description = description
        else:
            self.description = 'Malformed request'


class ServerError(Error):
    def __init__(self, description=None):
        if description is not None:
            self.description = description
        else:
            self.description = 'Server Error'
