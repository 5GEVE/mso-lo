import json
import os

from flask_script import Manager

from config import app, db
from models import NFVO, NFVO_CREDENTIALS

manager = Manager(app)
basedir = os.path.abspath(os.path.dirname(__file__))


@manager.command
def seed():
    SEED_NFVO = os.environ.get('DB_SEED_NFVO') or \
                os.path.join(basedir, 'seed/nfvo.json')
    SEED_NFVO_CRED = os.environ.get('DB_SEED_NFVO_CRED') or \
                     os.path.join(basedir, 'seed/nfvo_credentials.json')

    with open(SEED_NFVO, 'r') as f:
        nfvo_dict = json.load(f)

    for new_nfvo in nfvo_dict:
        new_nfvo_model = NFVO(**new_nfvo)
        db.session.add(new_nfvo_model)
        db.session.commit()

    with open(SEED_NFVO_CRED, 'r') as f:
        nfvo_cred_dict = json.load(f)

    for new_nfvo_cred in nfvo_cred_dict:
        new_nfvo_cred_model = NFVO_CREDENTIALS(**new_nfvo_cred)
        db.session.add(new_nfvo_cred_model)
        db.session.commit()


if __name__ == "__main__":
    manager.run()
