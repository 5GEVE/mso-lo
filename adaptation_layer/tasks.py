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
from typing import Dict
from urllib.error import HTTPError

import redis
from celery import Celery
from celery.utils.log import get_task_logger
from requests import post, RequestException

from adaptation_layer.driver.osm import OSM
from adaptation_layer.error_handler import ServerError, Error
from adaptation_layer.repository import iwf_repository

IWFREPO = os.getenv('IWFREPO', 'false').lower()
redis_host = os.getenv('REDIS_HOST') if os.getenv('REDIS_HOST') else 'redis'
redis_port = int(os.getenv('REDIS_PORT')) if os.getenv('REDIS_PORT') else 6379
# TTL for key in redis
KEY_TTL = 21600  # 6 hours

celery = Celery('tasks',
                broker='redis://{0}:{1}/0'.format(redis_host, redis_port),
                backend='redis://{0}:{1}/0'.format(redis_host, redis_port))

if IWFREPO == 'true':
    celery.conf.beat_schedule = {
        'add_post_osm_vims_periodic': {
            'task': 'adaptation_layer.tasks.post_osm_vims',
            'schedule': iwf_repository.interval
        },
        'add_osm_notifications': {
            'task': 'adaptation_layer.tasks.osm_notifications',
            'schedule': 5.0
        }
    }
celery.conf.timezone = 'UTC'
logger = get_task_logger(__name__)

redis_client = redis.Redis(
    host=redis_host, port=redis_port, db=1, decode_responses=True)


@celery.task
def post_osm_vims():
    osm_list = []
    try:
        osm_list = iwf_repository.find_nfvos_by_type('osm')
    except (ServerError, HTTPError) as e:
        logger.error(f'error with iwf repository: {str(e)}')
        logger.warning('skip post_osm_vims')
    for osm in osm_list:
        osm_vims = []
        if osm['credentials']:
            try:
                driver = OSM(iwf_repository.convert_nfvo_cred(osm))
                osm_vims, headers = driver.get_vim_list()
            except Error as e:
                logger.error('error contacting OSM at {0}:{1}: {2}'.format(
                    osm['credentials']['host'],
                    osm['credentials']['port'],
                    str(e)
                ))
                continue
        for v in osm_vims:
            try:
                iwf_repository.post_vim_safe(v, osm['_links']['self']['href'])
            except (ServerError, HTTPError)as e:
                logger.error(f'error with iwf repository: {str(e)}')
                logger.warning(f'skip vim: {v}')


@celery.task
def osm_notifications():
    osm_list = []
    try:
        osm_list = iwf_repository.find_nfvos_by_type('osm')
    except (ServerError, HTTPError)as e:
        logger.error(f'error with iwf repository: {str(e)}')
        logger.warning('skip osm notifications')
    for osm in osm_list:
        ops = []
        if osm['credentials']:
            try:
                driver = OSM(iwf_repository.convert_nfvo_cred(osm))
                ops, headers = driver.get_op_list({'args': {}})
            except Error as e:
                logger.error('error contacting OSM at {0}:{1}: {2}'.format(
                    osm['credentials']['host'],
                    osm['credentials']['port'],
                    str(e)
                ))
                continue
        for op in ops:
            last_s = redis_client.get(op['id'])
            logger.debug('last_s from redis: {}'.format(last_s))
            if not last_s or last_s != op['operationState']:
                logger.info('different op state, send notification')
                logger.debug('{},{}'.format(last_s, op['operationState']))
                redis_client.setex(op['id'], KEY_TTL, op['operationState'])
                notify_payload = {
                    "nsInstanceId": op['nsInstanceId'],
                    "nsLcmOpOccId": op['id'],
                    "operation": op['lcmOperationType'],
                    "notificationType": "NsLcmOperationOccurrenceNotification",
                    "timestamp": op['startTime'],
                    "operationState": op['operationState']
                }
                logger.debug(notify_payload)
                forward_notification.delay(notify_payload)


@celery.task
def forward_notification(notification: Dict):
    if IWFREPO == 'false':
        logger.warning('iwf repository disabled, ignore notification')
        return None
    subs = []
    try:
        subs = iwf_repository.search_subs_by_ns_instance(notification['nsInstanceId'])
    except (ServerError, HTTPError)as e:
        logger.error(f'error with iwf repository: {str(e)}')
        logger.warning('skip forward_notification')
        return
    if not subs:
        logger.warning('no subscriptions for nsInstanceId {0}'.format(
            notification['nsInstanceId']))
    for s in subs:
        try:
            if notification['notificationType'] in s['notificationTypes']:
                resp = post(s['callbackUri'], json=notification)
                resp.raise_for_status()
                logger.info(
                    'Notification sent to {0}'.format(s['callbackUri']))
        except RequestException as e:
            logger.error(
                'Cannot send notification to {0}: {1}'.format(s['callbackUri'], str(e)))
