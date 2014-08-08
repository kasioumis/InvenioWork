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
    id = db.Column(db.Integer(15, unsigned=True), nullable=False,
                server_default='0', primary_key=True)
    id_story = db.Column(db.Integer(15, unsigned=True), nullable=False,
                server_default='0')
    body = db.Column(db.String(512), nullable=False,
            server_default='0')
    target_element = db.Column(db.String(256), nullable=False,
            server_default='0')
    target_page = db.Column(db.String(256), nullable=False,
            server_default='0')
    nwsTOOLTIPcol = db.Column(db.String(45), nullable=False,
            server_default='0')


#def init_db(app):
#    db.init_app(app)
#    return app

