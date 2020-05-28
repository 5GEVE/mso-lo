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
from typing import Dict, List
from urllib.error import HTTPError

from celery import Celery
from requests import post, RequestException

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


@celery.task
def forward_notification(notification: Dict, subs: List[Dict]):
    logger = logging.getLogger('tasks.notifications')
    for s in subs:
        try:
            if notification['notificationType'] in s['notificationTypes']:
                resp = post(s['callbackUri'], json=notification)
                resp.raise_for_status()
                logger.info(
                    'Notification sent to {0}'.format(s['callbackUri']))
        except RequestException as e:
            logger.warning('Cannot send notification to {0}. Error: {1}'.format(
                s['callbackUri'], str(e)))
