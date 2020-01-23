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

from flask import jsonify, abort, request, make_response

import config
import driver.manager as manager
from error_handler import NfvoNotFound, NsNotFound, NsdNotFound
from error_handler import Unauthorized, BadRequest, ServerError, NsOpNotFound

app = config.app


@app.route('/nfvo', methods=['GET'])
def get_nfvo_list():
    try:
        nfvo_list = manager.get_nfvo_list(
            args={'args': request.args.to_dict()})
        return jsonify(nfvo_list)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>', methods=['GET'])
def get_nfvo(nfvo_id):
    try:
        nfvo = manager.get_nfvo(nfvo_id, args={'args': request.args.to_dict()})
        return jsonify(nfvo)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_instances', methods=['POST'])
def create_ns(nfvo_id):
    try:
        ns, headers = manager.get_driver(nfvo_id).create_ns(
            args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response(jsonify(ns), 201, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsdNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_instances', methods=['GET'])
def get_ns_list(nfvo_id):
    try:
        ns_list, headers = manager.get_driver(nfvo_id).get_ns_list(
            args={'args': request.args.to_dict()})
        return make_response(jsonify(ns_list), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_instances/<ns_id>', methods=['GET'])
def get_ns(nfvo_id, ns_id):
    try:
        ns, headers = manager.get_driver(nfvo_id).get_ns(
            ns_id, args={'args': request.args.to_dict()})
        return make_response(jsonify(ns), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_instances/<ns_id>', methods=['DELETE'])
def delete_ns(nfvo_id, ns_id):
    try:
        empty_body, headers = manager.get_driver(nfvo_id).delete_ns(
            ns_id, args={'args': request.args.to_dict()})
        return make_response('', 202, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_instances/<ns_id>/instantiate', methods=['POST'])
def instantiate_ns(nfvo_id, ns_id):
    try:
        empty_body, headers = manager.get_driver(nfvo_id). \
            instantiate_ns(ns_id, args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response('', 202, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_instances/<ns_id>/terminate', methods=['POST'])
def terminate_ns(nfvo_id, ns_id):
    try:
        empty_body, headers = manager.get_driver(nfvo_id).terminate_ns(
            ns_id, args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response('', 202, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_instances/<ns_id>/scale', methods=['POST'])
def scale_ns(nfvo_id, ns_id):
    try:
        empty_body, headers = manager.get_driver(nfvo_id).scale_ns(
            ns_id, args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response('', 202, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_lcm_op_occs', methods=['GET'])
def get_op_list(nfvo_id):
    try:
        op_list, headers = manager.get_driver(nfvo_id).get_op_list(
            args={'args': request.args.to_dict()})
        return make_response(jsonify(op_list), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns_lcm_op_occs/<nsLcmOpId>', methods=['GET'])
def get_op(nfvo_id, nsLcmOpId):
    try:
        ns_op, headers = manager.get_driver(nfvo_id).get_op(
            nsLcmOpId, args={'args': request.args.to_dict()})
        return make_response(jsonify(ns_op), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsOpNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
