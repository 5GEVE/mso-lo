from flask import Flask, jsonify, abort
import driver.manager as manager

app = Flask(__name__)


@app.route('/nfvo', methods=['GET'])
def get_nfvo_list():
    nfvo_list = manager.get_nfvo_list()
    return jsonify(nfvo_list)


@app.route('/nfvo/<nfvo_id>', methods=['GET'])
def get_nfvo(nfvo_id):
    nfvo = manager.get_nfvo(nfvo_id)
    return jsonify(nfvo)


@app.route('/nfvo/<nfvo_id>/nsd', methods=['GET'])
def get_nsd_list(nfvo_id):
    nsds = manager.get_driver(nfvo_id).get_nsd_list()
    return jsonify(nsds)


@app.route('/nfvo/<nfvo_id>/nsd', methods=['POST'])
def onboard_nsd(nfvo_id):
    nsd = manager.get_driver(nfvo_id).onboard_nsd()
    return jsonify(nsd)


@app.route('/nfvo/<nfvo_id>/nsd/<nsd_info_id>', methods=['GET'])
def get_nsd(nfvo_id, nsd_info_id):
    nsd = manager.get_driver(nfvo_id).get_nsd(nsd_info_id)
    if not nsd:
        abort(404)
    return jsonify(nsd)


@app.route('/nfvo/<nfvo_id>/nsd/<nsd_info_id>', methods=['PUT'])
def update_nsd(nfvo_id, nsd_info_id):
    # TODO missing nsd data
    nsd = manager.get_driver(nfvo_id).update_nsd(nsd_info_id)
    if not nsd:
        abort(404)
    return jsonify(nsd)


@app.route('/nfvo/<nfvo_id>/nsd/<nsd_info_id>', methods=['DELETE'])
def delete_nsd(nfvo_id, nsd_info_id):
    nsd = manager.get_driver(nfvo_id).update_nsd(nsd_info_id)
    if not nsd:
        abort(404)
    return jsonify(nsd)


@app.route('/nfvo/<nfvo_id>/vnfd', methods=['GET'])
def get_vnfd_list(nfvo_id):
    vnfd_list = manager.get_driver(nfvo_id).get_vnfd_list()
    return jsonify(vnfd_list)


@app.route('/nfvo/<nfvo_id>/vnfd/<vnfd_id>', methods=['GET'])
def get_vnfd(nfvo_id, vnfd_id):
    vnfd = manager.get_driver(nfvo_id).get_vnfd(vnfd_id)
    if not vnfd:
        abort(404)
    return jsonify(vnfd)


@app.route('/nfvo/<nfvo_id>/pnfd', methods=['GET'])
def get_pnfd_list(nfvo_id):
    pnfd_list = manager.get_driver(nfvo_id).get_pnfd_list()
    return jsonify(pnfd_list)


@app.route('/nfvo/<nfvo_id>/pnfd/<pnfd_id>', methods=['GET'])
def get_pnfd(nfvo_id, pnfd_id):
    pnfd = manager.get_driver(nfvo_id).get_pnfd(pnfd_id)
    if not pnfd:
        abort(404)
    return jsonify(pnfd)


if __name__ == '__main__':
    app.run(debug=True)
