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
        app.logger.error('error: {}'.format(error.description))
        return make_response(jsonify({'error': error.description}), 400)

    @app.errorhandler(401)
    def unauthorized(error):
        app.logger.error('error: {}'.format(error.description))
        return make_response(jsonify({'error': error.description}), 401)

    @app.errorhandler(404)
    def not_found(error):
        app.logger.error('error: {}'.format(error.description))
        return make_response(jsonify({'error': error.description}), 404)

    @app.errorhandler(500)
    def server_error(error):
        app.logger.error('error: {}'.format(error.description))
        return make_response(jsonify({'error': error.description}), 500)


class Error(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, description='Generic Error'):
        self.description = description


class NfvoNotFound(Error):
    def __init__(self, nfvo_id):
        super().__init__(description='NFVO {0} not found.'.format(nfvo_id))


class NfvoCredentialsNotFound(Error):
    def __init__(self, nfvo_id):
        super().__init__(
            description='Credentials not found for NFVO {0}.'.format(nfvo_id))


class VimNotFound(Error):
    def __init__(self):
        super().__init__(description='Vim not found.')


class NsOpNotFound(Error):
    def __init__(self, ns_op_id=None):
        super().__init__('NS LCM operation {0} not found.'.format(ns_op_id))


class NsNotFound(Error):
    def __init__(self, ns_id=None):
        super().__init__('NS instance {0} not found.'.format(ns_id))


class NsdNotFound(Error):
    def __init__(self, nsd_id=None):
        super().__init__('NS descriptor {0} not found.'.format(nsd_id))


class VnfNotFound(Error):
    def __init__(self, vnf_id=None):
        super().__init__('VNF instance {0} not found.'.format(vnf_id))


class VnfPkgNotFound(Error):
    def __init__(self, vnfpkg_id=None):
        super().__init__('VNF package {0} not found.'.format(vnfpkg_id))


class SubscriptionNotFound(Error):
    def __init__(self, sub_id=None):
        super().__init__('Subscription {0} not found.'.format(sub_id))


class BadRequest(Error):
    def __init__(self, description='Bad request'):
        super().__init__(description=description)


class Unauthorized(Error):
    def __init__(self, description='Unauthorized'):
        super().__init__(description=description)


class Forbidden(Error):
    def __init__(self, description='Forbidden'):
        super().__init__(description=description)


class ResourceNotFound(Error):
    def __init__(self, description='Resource not found.'):
        super().__init__(description=description)


class MethodNotAllowed(Error):
    def __init__(self, description='Method Not Allowed'):
        super().__init__(description=description)


class Conflict(Error):
    def __init__(self, description='Conflict'):
        super().__init__(description=description)


class Unprocessable(Error):
    def __init__(self, description='Unprocessable Entity'):
        super().__init__(description=description)


class ServerError(Error):
    def __init__(self, description=None):
        super().__init__(description=description)
