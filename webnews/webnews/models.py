"""
nwsToolTip database models.
"""
# General imports.
from invenio.ext.sqlalchemy import db
from sqlalchemy.ext.associationproxy import association_proxy
from invenio.modules.accounts.models import User
from invenio.modules.baskets.models import BskBASKET
from invenio.modules.search.models import WebQuery
import pickle
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin






class NwsSTORY(db.Model):
    """Represents a nwsSTORY record."""
    __tablename__ = 'nwsSTORY'
    id = db.Column(db.Integer(11, unsigned=True), nullable=False, primary_key=True,autoincrement=True)
    title = db.Column(db.String(256), nullable=False, default='')
    body = db.Column(db.Text, nullable=False, default='')
    created = db.Column(db.TIMESTAMP, nullable=False)
    document_status=db.Column(db.String(45), nullable=False, default='SHOW')
    remote_ip=db.Column(db.String(100), nullable=False, default='0.0.0.0')
    email=db.Column(db.String(100), nullable=False, default='admin@admin.com')
    nickname=db.Column(db.String(100), nullable=False, default='admin')
    uid=db.Column(db.Integer(11, unsigned=True), nullable=False)
    nwsToolTip = db.relationship('NwsToolTip', backref='nwsSTORY',cascade='all, delete, delete-orphan')
    nwsTAG = db.relationship('NwsTAG', backref='nwsSTORY',cascade='all, delete, delete-orphan')


class NwsToolTip(db.Model):
    """Represents a NwsToolTip record."""
    __tablename__ = 'nwsTOOLTIP'
    id = db.Column(db.Integer(15, unsigned=True), nullable=False, primary_key=True,autoincrement=True)
    id_story = db.Column(db.Integer(15, unsigned=True), db.ForeignKey('nwsSTORY.id'))
    body = db.Column(db.String(512), nullable=False, server_default='0')
    target_element = db.Column(db.String(256), nullable=False,server_default='0')
    target_page = db.Column(db.String(256), nullable=False)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'id_story': self.id_story,
           'body': self.body,
           'target_element': self.target_element,
           'target_page': self.target_page

       }
    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializeable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.nwsSTORY]



class NwsTAG(db.Model):
    """Represents a nwsTAG record."""
    __tablename__ = 'nwsTAG'
    id = db.Column(db.Integer(15, unsigned=True), nullable=False, primary_key=True,autoincrement=True)
    id_story = db.Column(db.Integer(15, unsigned=True), db.ForeignKey('nwsSTORY.id'))
    tag = db.Column(db.String(64), nullable=False, default='')


    @property
    def serialize_tag(self):
       """Return object data in easily serializeable format"""
       return {
           'id_story': self.id_story


       }
