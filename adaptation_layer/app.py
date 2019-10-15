from flask import Flask, jsonify, abort, request, make_response
import driver.manager as manager
from error_handler import init_errorhandler, NfvoNotFound, NsNotFound, Unauthorized, BadRequest

app = Flask(__name__)
init_errorhandler(app)


@app.route('/nfvo', methods=['GET'])
def get_nfvo_list():
    try:
        nfvo_list = manager.get_nfvo_list(args={'args': request.args.to_dict()})
        return jsonify(nfvo_list)
    except Unauthorized as e:
        abort(401, description=e.description)


@app.route('/nfvo/<nfvo_id>', methods=['GET'])
def get_nfvo(nfvo_id):
    try:
        nfvo = manager.get_nfvo(nfvo_id, args={'args': request.args.to_dict()})
        return jsonify(nfvo)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns', methods=['GET'])
def get_ns_list(nfvo_id):
    try:
        ns_list = manager.get_driver(nfvo_id).get_ns_list(args={'args': request.args.to_dict()})
        return jsonify(ns_list)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns', methods=['POST'])
def create_ns(nfvo_id):
    try:
        ns = manager.get_driver(nfvo_id).create_ns(args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response(jsonify(ns), 201)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns/<ns_id>/instantiate', methods=['post'])
def instantiate_ns(nfvo_id, ns_id):
    try:
        ns = manager.get_driver(nfvo_id).instantiate_ns(ns_id, args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response(jsonify(ns), 202)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns/<ns_id>/terminate', methods=['post'])
def terminate_ns(nfvo_id, ns_id):
    try:
        ns = manager.get_driver(nfvo_id).terminate_ns(ns_id, args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response(ns, code=202)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns/<ns_id>', methods=['GET'])
def get_ns(nfvo_id, ns_id):
    try:
        ns = manager.get_driver(nfvo_id).get_ns(ns_id, args={'args': request.args.to_dict()})
        return jsonify(ns)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)


@app.route('/nfvo/<nfvo_id>/ns/<ns_id>/scale', methods=['POST'])
def scale_ns(nfvo_id, ns_id):
    try:
        ns = manager.get_driver(nfvo_id).scale_ns(ns_id, args={'payload': request.json, 'args': request.args.to_dict()})
        return make_response(ns, code=202)
    except BadRequest as e:
        abort(400, description=e.description)
    except Unauthorized as e:
        abort(401, description=e.description)
    except NfvoNotFound as e:
        abort(404, description=e.description)
    except NsNotFound as e:
        abort(404, description=e.description)


if __name__ == '__main__':
    app.run(debug=True)
