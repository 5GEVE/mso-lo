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

import os
from flask_migrate import Migrate
from adaptation_layer.repository import sqlite, iwf_repository
from flask import current_app, _app_ctx_stack


class MsoloDB(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.teardown_appcontext(self.teardown)
        IWFREPO = os.getenv('IWFREPO', 'false').lower()
        if IWFREPO == 'true':
            self.app.logger.info('using iwf repository')
            self.msolo_db = iwf_repository
        else:
            self.app.logger.info('using sqlite')
            sqlite.db.init_app(self.app)
            basedir = os.path.abspath(os.path.dirname(__file__))
            MIGRATION_DIR = os.path.join(basedir, 'migrations')
            migrate = Migrate(self.app, sqlite.db, directory=MIGRATION_DIR)
            self.msolo_db = sqlite

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'msolo_db'):
            del ctx.msolo_db
