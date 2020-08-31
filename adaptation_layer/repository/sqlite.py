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

import datetime
from typing import List, Dict

from flask_sqlalchemy import SQLAlchemy

from adaptation_layer.error_handler import NfvoNotFound, RanoNotFound

db = SQLAlchemy()


class NFVO(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(128), nullable=False)
    type = db.Column('type', db.String(128), nullable=False)
    site = db.Column('site', db.String(128), nullable=False)
    uri = db.Column('uri', db.String(128))
    created_at = db.Column('created_at', db.DateTime,
                           default=datetime.datetime.utcnow())
    updated_at = db.Column('updated_at', db.DateTime,
                           default=datetime.datetime.utcnow())

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'site': self.site,
            'uri': self.uri,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }

    def __init__(self, **kwargs):
        super(NFVO, self).__init__(**kwargs)

    def __repr__(self):
        return '<NFVO {}>'.format(self.id)


class NFVO_CREDENTIALS(db.Model):
    nfvo_id = db.Column('nfvo_id', db.Integer, db.ForeignKey(
        'NFVO.id'), primary_key=True)
    host = db.Column('host', db.String(128), nullable=False)
    project = db.Column('project', db.String(128), nullable=False)
    user = db.Column('user', db.String(128), nullable=False)
    password = db.Column('password', db.String(128), nullable=False)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'nfvo_id': self.nfvo_id,
            'host': self.host,
            'project': self.project,
            'user': self.user,
            'password': self.password
        }


class RANO(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(128), nullable=False)
    type = db.Column('type', db.String(128), nullable=False)
    site = db.Column('site', db.String(128), nullable=False)
    uri = db.Column('uri', db.String(128))

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'site': self.site,
            'uri': self.uri,
        }

    def __init__(self, **kwargs):
        super(RANO, self).__init__(**kwargs)

    def __repr__(self):
        return '<RANO {}>'.format(self.id)


class RANO_CREDENTIALS(db.Model):
    rano_id = db.Column('rano_id', db.Integer, db.ForeignKey('RANO.id'), primary_key=True)
    host = db.Column('host', db.String(128), nullable=False)
    project = db.Column('project', db.String(128), nullable=False)
    user = db.Column('user', db.String(128), nullable=False)
    password = db.Column('password', db.String(128), nullable=False)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'rano_id': self.rano_id,
            'host': self.host,
            'project': self.project,
            'user': self.user,
            'password': self.password
        }


def get_nfvo_by_id(nfvo_id: int) -> Dict:
    nfvo = NFVO.query.filter_by(id=nfvo_id).first()
    if nfvo is None:
        raise NfvoNotFound(nfvo_id=nfvo_id)
    return nfvo.serialize


def get_rano_by_id(rano_id: int) -> Dict:
    rano = RANO.query.filter_by(id=rano_id).first()
    if rano is None:
        raise RanoNotFound(rano_id=rano_id)
    return rano.serialize


def get_nfvo_list() -> List[Dict]:
    return [nfvo.serialize for nfvo in NFVO.query.all()]


def get_rano_list() -> List[Dict]:
    return [rano.serialize for rano in RANO.query.all()]


def get_nfvo_cred(nfvo_id: int) -> Dict:
    nfvo_cred = NFVO_CREDENTIALS.query.filter_by(nfvo_id=nfvo_id).first()
    if nfvo_cred is None:
        raise NfvoNotFound(nfvo_id=nfvo_id)
    return nfvo_cred.serialize


def get_subscription_list(nfvo_id: int) -> Dict:
    raise NotImplementedError("The method is not implemented")


def create_subscription(nfvo_id: int, body: Dict) -> Dict:
    raise NotImplementedError("The method is not implemented")


def get_subscription(nfvo_id: int, subscriptionId: int) -> Dict:
    raise NotImplementedError("The method is not implemented")


def delete_subscription(subscriptionId: int) -> None:
    raise NotImplementedError("The method is not implemented")


def search_subs_by_ns_instance(ns_instance_id: str) -> List[Dict]:
    raise NotImplementedError("The method is not implemented")
