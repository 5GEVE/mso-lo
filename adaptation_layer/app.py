from flask import Flask, jsonify, abort
import driver.manager as manager

app = Flask(__name__)


@app.route('/nfvo/<nfvo_id>/nsd', methods=['GET'])
def get_nsd_list(nfvo_id):
    nsds = manager.get_driver(nfvo_id).get_nsd_list(nfvo_id)
    return jsonify(nsds)


@app.route('/nfvo/<nfvo_id>/nsd/<nsd_id>', methods=['GET'])
def get_nsd(nfvo_id, nsd_id):
    nsd = manager.get_driver(nfvo_id).get_nsd(nfvo_id, nsd_id)
    if not nsd:
        abort(404)
    return jsonify(nsd)


if __name__ == '__main__':
    app.run(debug=True)
