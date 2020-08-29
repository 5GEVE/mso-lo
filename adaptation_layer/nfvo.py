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

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify,
    abort, make_response
)
from adaptation_layer.error_handler import Unauthorized, BadRequest, \
    ServerError, ResourceNotFound
import json
from adaptation_layer import database
bp = Blueprint('nfvo', __name__, url_prefix='/nfvo')


@bp.route('/', methods=['GET'])
def get_nfvo_list():
    try:
        return make_response(jsonify(database.msolo_db.get_nfvo_list()), 200)
    except Unauthorized as e:
        abort(401, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>', methods=['GET'])
def get_nfvo(nfvo_id):
    try:
        return make_response(
            jsonify(database.msolo_db.get_nfvo_by_id(nfvo_id)), 200)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_instances', methods=['POST'])
def create_ns(nfvo_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        ns, headers = driver.create_ns(
            args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response(jsonify(ns), 201, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except Forbidden as e:
        abort(403, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, NsdNotFound) as e:
        abort(404, description=e.description)
    except Conflict as e:
        abort(409, description=e.description)
    except Unprocessable as e:
        abort(422, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_instances', methods=['GET'])
def get_ns_list(nfvo_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        ns_list, headers = driver.get_ns_list(
            args={'args': request.args.to_dict()})
        return make_response(jsonify(ns_list), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound) as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_instances/<ns_id>', methods=['GET'])
def get_ns(nfvo_id, ns_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        ns, headers = driver.get_ns(
            ns_id, args={'args': request.args.to_dict()})
        return make_response(jsonify(ns), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, NsNotFound) as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_instances/<ns_id>', methods=['DELETE'])
def delete_ns(nfvo_id, ns_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        empty_body, headers = driver.delete_ns(
            ns_id, args={'args': request.args.to_dict()})
        return make_response('', 204, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except Forbidden as e:
        abort(403, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, NsNotFound) as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_instances/<ns_id>/instantiate', methods=['POST'])
def instantiate_ns(nfvo_id, ns_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        empty_body, headers = driver.instantiate_ns(
            ns_id,
            args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response('', 202, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except Forbidden as e:
        abort(403, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, NsNotFound) as e:
        abort(404, description=e.description)
    except Conflict as e:
        abort(409, description=e.description)
    except Unprocessable as e:
        abort(422, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_instances/<ns_id>/terminate', methods=['POST'])
def terminate_ns(nfvo_id, ns_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        empty_body, headers = driver.terminate_ns(
            ns_id,
            args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response('', 202, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except Forbidden as e:
        abort(403, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, NsNotFound) as e:
        abort(404, description=e.description)
    except Conflict as e:
        abort(409, description=e.description)
    except Unprocessable as e:
        abort(422, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_instances/<ns_id>/scale', methods=['POST'])
def scale_ns(nfvo_id, ns_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        empty_body, headers = driver.scale_ns(
            ns_id,
            args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response('', 202, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except Forbidden as e:
        abort(403, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, NsNotFound) as e:
        abort(404, description=e.description)
    except Conflict as e:
        abort(409, description=e.description)
    except Unprocessable as e:
        abort(422, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_lcm_op_occs', methods=['GET'])
def get_op_list(nfvo_id):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        op_list, headers = driver.get_op_list(
            args={'args': request.args.to_dict()})
        return make_response(jsonify(op_list), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, NsNotFound) as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/ns_lcm_op_occs/<nsLcmOpId>', methods=['GET'])
def get_op(nfvo_id, nsLcmOpId):
    try:
        driver = manager.get_driver(nfvo_id, database.msolo_db)
        ns_op, headers = driver.get_op(
            nsLcmOpId, args={'args': request.args.to_dict()})
        return make_response(jsonify(ns_op), 200, headers)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound,
            NsNotFound, NsOpNotFound) as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/subscriptions', methods=['GET'])
def get_subscription_list(nfvo_id):
    try:
        return make_response(
            jsonify(database.msolo_db.get_subscription_list(nfvo_id)),
            200)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/subscriptions', methods=['POST'])
def create_subscription(nfvo_id):
    try:
        return make_response(
            jsonify(database.msolo_db.create_subscription(nfvo_id,
                                                          request.json)), 201)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except Forbidden as e:
        abort(403, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound) as e:
        abort(404, description=e.description)
    except Conflict as e:
        abort(409, description=e.description)
    except Unprocessable as e:
        abort(422, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/subscriptions/<subscriptionId>', methods=['GET'])
def get_subscription(nfvo_id, subscriptionId):
    try:
        return make_response(
            jsonify(database.msolo_db.get_subscription(
                nfvo_id, subscriptionId)),
            200)
    except Unauthorized as e:
        abort(401, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, SubscriptionNotFound) as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/subscriptions/<subscriptionId>', methods=['DELETE'])
def delete_subscription(nfvo_id, subscriptionId):
    try:
        database.msolo_db.delete_subscription(subscriptionId)
        return make_response('', 204)
    except Unauthorized as e:
        abort(401, description=e.description)
    except (NfvoNotFound, NfvoCredentialsNotFound, SubscriptionNotFound) as e:
        abort(404, description=e.description)
    except ServerError as e:
        abort(500, description=e.description)


@bp.route('/<nfvo_id>/notifications', methods=['POST'])
def post_notification(nfvo_id):
    required = ('nsInstanceId', 'operation', 'operationState')
    if not all(k in request.json for k in required):
        abort(400, 'One of {0} is missing'.format(str(required)))
    tasks.forward_notification.delay(request.json)
    return make_response('', 204)
