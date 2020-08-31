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
import logging
import os

import click
from flask import Flask
from flask.cli import with_appcontext

from adaptation_layer.repository.sqlite import NFVO, NFVO_CREDENTIALS, RANO, \
    RANO_CREDENTIALS
# import sqlite
from . import tasks
from .config import Config
from .db import MsoloDB
from .error_handler import init_errorhandler

database = MsoloDB()


def create_app(test_config=None):

    # import blueprints
    from . import app as mso_lo_app

    logging.basicConfig(level=logging.INFO)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    init_errorhandler(app)
    database.init_app(app)
    IWFREPO = os.getenv('IWFREPO', 'false').lower()
    if IWFREPO == 'true':
        tasks.post_osm_vims.delay()
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.url_map.strict_slashes = False
    app.cli.add_command(my_command)

    # register blueprints
    app.register_blueprint(mso_lo_app.nfvo_bp)
    app.register_blueprint(mso_lo_app.rano_bp)

    return app


@click.command('seed')
@with_appcontext
def my_command():
    basedir = os.path.abspath(os.path.dirname(__file__))
    SEED_NFVO = os.environ.get('DB_SEED_NFVO') or \
                os.path.join(basedir, 'seed/nfvo.json')
    SEED_NFVO_CRED = os.environ.get('DB_SEED_NFVO_CRED') or \
                     os.path.join(basedir, 'seed/nfvo_credentials.json')
    SEED_RANO = os.environ.get('DB_SEED_RANO') or \
                os.path.join(basedir, 'seed/rano.json')
    SEED_RANO_CRED = os.environ.get('DB_SEED_RANO_CRED') or \
                     os.path.join(basedir, 'seed/rano_credentials.json')

    with open(SEED_NFVO, 'r') as f:
        nfvo_dict = json.load(f)

    for new_nfvo in nfvo_dict:
        new_nfvo_model = NFVO(**new_nfvo)
        database.msolo_db.db.session.add(new_nfvo_model)
        database.msolo_db.db.session.commit()

    with open(SEED_NFVO_CRED, 'r') as f:
        nfvo_cred_dict = json.load(f)

    for new_nfvo_cred in nfvo_cred_dict:
        new_nfvo_cred_model = NFVO_CREDENTIALS(**new_nfvo_cred)
        database.msolo_db.db.session.add(new_nfvo_cred_model)
        database.msolo_db.db.session.commit()

    with open(SEED_RANO, 'r') as f:
        rano_dict = json.load(f)

    for new_rano in rano_dict:
        new_rano_model = RANO(**new_rano)
        database.msolo_db.db.session.add(new_rano_model)
        database.msolo_db.db.session.commit()

    with open(SEED_RANO_CRED, 'r') as f:
        rano_cred_dict = json.load(f)

    for new_rano_cred in rano_cred_dict:
        new_rano_cred_model = RANO_CREDENTIALS(**new_rano_cred)
        database.msolo_db.db.session.add(new_rano_cred_model)
        database.msolo_db.db.session.commit()
