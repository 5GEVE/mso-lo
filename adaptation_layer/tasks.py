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
from urllib.error import HTTPError

from celery import Celery

from error_handler import ServerError

# TODO config
celery = Celery('tasks', broker='redis://localhost:6379',
                backend='redis://localhost:6379')

# Run worker with: celery -A tasks worker --loglevel=info -B
celery.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.post_osm_vims_thread',
        'schedule': 2.0
    },
}
celery.conf.timezone = 'UTC'


@celery.task
def post_osm_vims_thread():
    try:
        # post_osm_vims()
        print('aaaaaaaa')
        return 'vaffa'
    except (ServerError, HTTPError)as e:
        pass
        # logger.warning('error with siteinventory. skip post_osm_vims')
        # logger.warning(e)
