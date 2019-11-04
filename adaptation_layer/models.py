import sys
from app import db
import datetime
from collections import OrderedDict


class NFVO(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(128), nullable=False)
    nfvo_type = db.Column('type', db.String(128), nullable=False)
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
            'type': self.nfvo_type,
            'site': self.site,
            'uri': self.uri,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return '<NFVO {}>'.format(self.id)


class NFVO_CREDENTIALS(db.Model):
    nfvo_id = db.Column('id', db.Integer, db.ForeignKey(
        'NFVO.id'), primary_key=True)
    host = db.Column('host', db.String(128), nullable=False)
    project = db.Column('project', db.String(128), nullable=False)
    user = db.Column('user', db.String(128), nullable=False)
    password = db.Column('password', db.String(128), nullable=False)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.nfvo_id,
            'host': self.host,
            'project': self.project,
            'user': self.user,
            'password': self.password
        }
