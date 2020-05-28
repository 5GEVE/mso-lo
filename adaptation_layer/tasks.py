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
from typing import Dict, List
from urllib.error import HTTPError

from celery import Celery
from celery.utils.log import get_task_logger
from requests import post, RequestException

import siteinventory
from driver.osm import OSM
from error_handler import ServerError, Error

redis_host = os.getenv('REDIS_HOST') if os.getenv('REDIS_HOST') else 'redis'
redis_port = int(os.getenv('REDIS_PORT')) if os.getenv('REDIS_PORT') else 6379
celery = Celery('tasks',
                broker='redis://{0}:{1}'.format(redis_host, redis_port),
                backend='redis://{0}:{1}'.format(redis_host, redis_port))

celery.conf.beat_schedule = {
    'add_post_osm_vims_periodic': {
        'task': 'tasks.post_osm_vims',
        'schedule': siteinventory.interval
    },
}
celery.conf.timezone = 'UTC'
logger = get_task_logger(__name__)


@celery.task
def post_osm_vims():
    try:
        osm_list = siteinventory.find_nfvos_by_type('osm')
        for osm in osm_list:
            if osm['credentials']:
                try:
                    driver = OSM(siteinventory.convert_cred(osm))
                    osm_vims, headers = driver.get_vim_list()
                except Error as e:
                    logger.warning(
                        'error contacting osm {0}:{1}'.format(
                            osm['credentials']['host'],
                            osm['credentials']['port'],
                        ))
                    logger.warning(e)
                    continue
                for v in osm_vims:
                    siteinventory.post_vim_safe(v,
                                                osm['_links']['self']['href'])
    except (ServerError, HTTPError)as e:
        logger.warning('error with siteinventory. skip post_osm_vims')
        logger.warning(e)


@celery.task
def forward_notification(notification: Dict, subs: List[Dict]):
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
