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
from .config import Config
from .repository import sqlite, iwf_repository
# import sqlite
# import tasks

from flask import Flask, jsonify

from flask_migrate import Migrate
from .error_handler import init_errorhandler


def create_app(test_config=None):

    from . import nfvo

    IWFREPO = os.getenv('IWFREPO', 'false').lower()

    logging.basicConfig(level=logging.INFO)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    init_errorhandler(app)

    app.config['CORS_HEADERS'] = 'Content-Type'

    if IWFREPO == 'true':
        app.logger.info('using iwf repository')
        database = iwf_repository
        # tasks.post_osm_vims.delay()
    else:
        app.logger.info('using sqlite')
        sqlite.db.init_app(app)
        migrate = Migrate(app, sqlite.db)
        database = sqlite

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(nfvo.bp)

    return app
