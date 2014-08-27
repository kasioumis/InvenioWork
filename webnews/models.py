"""
nwsToolTip database models.
"""
# General imports.
from invenio.ext.sqlalchemy import db
from sqlalchemy.ext.associationproxy import association_proxy

# Create your models here.
from invenio.modules.accounts.models import User
from invenio.modules.baskets.models import BskBASKET
from invenio.modules.search.models import WebQuery




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



class NwsSTORY(db.Model):
    """Represents a nwsSTORY record."""
    __tablename__ = 'nwsSTORY'
    id = db.Column(db.Integer(15, unsigned=True), nullable=False, primary_key=True,autoincrement=True)
    title = db.Column(db.String(256), nullable=False, default='')
    body = db.Column(db.Text, nullable=False, default='')
    created = db.Column(db.TIMESTAMP, nullable=False, server_default='9999-12-31 23:59:59')
    document_status=db.Column(db.String(45), nullable=False, default='SHOW')
    nwsToolTip = db.relationship('NwsToolTip', backref='nwsSTORY' )
    nwsTAG = db.relationship('NwsTAG', backref='nwsSTORY' )

class NwsTAG(db.Model):
    """Represents a nwsTAG record."""
    __tablename__ = 'nwsTAG'
    id = db.Column(db.Integer(15, unsigned=True), nullable=False, primary_key=True,autoincrement=True)
    id_story = db.Column(db.Integer(15, unsigned=True), db.ForeignKey('nwsSTORY.id'))
    tag = db.Column(db.String(64), nullable=False, default='')



#def init_db(app):
#    db.init_app(app)
#    return app

