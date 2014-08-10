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
    id = db.Column(db.Integer(15, unsigned=True), nullable=False, server_default='0', primary_key=True,autoincrement=True)
    id_story = db.Column(db.Integer(15, unsigned=True), db.ForeignKey('nwsSTORY.id'))
    body = db.Column(db.String(512), nullable=False, server_default='0')
    target_element = db.Column(db.String(256), nullable=False,server_default='0')
    target_page = db.Column(db.String(256), nullable=False)

class NwsSTORY(db.Model):
    """Represents a nwsSTORY record."""
    __tablename__ = 'nwsSTORY'
    id = db.Column(db.Integer(15, unsigned=True), nullable=False, primary_key=True,autoincrement=True)
    title = db.Column(db.String(256), nullable=False, default='')
    body = db.Column(db.Text, nullable=False, default='')
    created = db.Column(db.TIMESTAMP, nullable=False, server_default='9999-12-31 23:59:59')
    nwsToolTip = db.relationship('NwsToolTip',uselist=False, backref='nwsSTORY' )


#def init_db(app):
#    db.init_app(app)
#    return app

