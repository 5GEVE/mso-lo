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

import json
import os

from flask_script import Manager

from app import app
from data.sqlite import db, NFVO, NFVO_CREDENTIALS

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
