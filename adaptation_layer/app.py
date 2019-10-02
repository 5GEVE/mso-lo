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


@app.route('/nfvo/<nfvo_id>/ns', methods=['GET'])
def get_ns_list(nfvo_id):
    nsds = manager.get_driver(nfvo_id).get_ns_list()
    return jsonify(nsds)


@app.route('/nfvo/<nfvo_id>/ns/<ns_id>', methods=['GET'])
def get_ns(nfvo_id, ns_id):
    ns = manager.get_driver(nfvo_id).get_ns(ns_id)
    if not ns:
        abort(404)
    return jsonify(ns)

@app.route('/nfvo/<nfvo_id>/vnf', methods=['GET'])
def get_vnf_list(nfvo_id):
    vnf_list = manager.get_driver(nfvo_id).get_vnf_list()
    return jsonify(vnf_list)


@app.route('/nfvo/<nfvo_id>/vnf/<vnf_id>', methods=['GET'])
def get_vnf(nfvo_id, vnf_id):
    vnf = manager.get_driver(nfvo_id).get_vnf(vnf_id)
    if not vnf:
        abort(404)
    return jsonify(vnf)




if __name__ == '__main__':
    app.run(debug=True)
