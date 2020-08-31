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

import logging
import os
import click
import json
from .config import Config
from flask.cli import with_appcontext
from flask import current_app

from adaptation_layer.repository.sqlite import NFVO, NFVO_CREDENTIALS
# import sqlite
from . import tasks

from flask import Flask, jsonify
from .db import MsoloDB
from .error_handler import init_errorhandler

database = MsoloDB()


def create_app(test_config=None):

    # import blueprints
    from . import nfvo

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
    app.register_blueprint(nfvo.nfvo_bp)
    app.register_blueprint(nfvo.rano_bp)

    return app


@click.command('seed')
@with_appcontext
def my_command():
    basedir = os.path.abspath(os.path.dirname(__file__))
    SEED_NFVO = os.environ.get('DB_SEED_NFVO') or \
        os.path.join(basedir, 'seed/nfvo.json')
    SEED_NFVO_CRED = os.environ.get('DB_SEED_NFVO_CRED') or \
        os.path.join(basedir, 'seed/nfvo_credentials.json')

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
