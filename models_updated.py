from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta, datetime

from invenio.ext.sqlalchemy import db
from invenio.webnews_config import CFG_WEBNEWS_TOOLTIPS_COOKIE_LONGEVITY
from invenio.webnews_utils import convert_xpath_expression_to_jquery_selector

Base = declarative_base()
mysql_db = create_engine('mysql://login:password@localhost/name_database', echo=True)
connection = mysql_db.connect()

# MODEL DEFINITION

class nwsSTORY(db.Model):
    """
    CREATE TABLE 'nwsSTORY' (
     'id' int(11) NOT NULL AUTO_INCREMENT,
     'title' varchar(256) NOT NULL,
     'body' text NOT NULL,
     'created' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ('id')
    );
    """
    __tablename__ = 'nwsSTORY'

    id = db.Column(db.Integer(11), nullable=False, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())

class nwsTAG(db.Model):
    """
    CREATE TABLE 'nwsTAG' (
     'id' int(11) NOT NULL AUTO_INCREMENT,
     'tag' varchar(64) NOT NULL,
     PRIMARY KEY ('id')
    );
    """
    __tablename__ = 'nwsTAG'

    id = db.Column(db.Integer(11), nullable=False, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(64), nullable=False)

class nwsTOOLTIP(db.Model):
    """
    CREATE TABLE 'nwsTOOLTIP' (
     'id' int(11) NOT NULL AUTO_INCREMENT,
     'id_story' int(11) NOT NULL,
     'body' varchar(512) NOT NULL,
     'target_element' varchar(256) NOT NULL DEFAULT '',
     'target_page' varchar(256) NOT NULL DEFAULT '',
     PRIMARY KEY ('id'),
     KEY 'id_story' ('id_story'),
     CONSTRAINT 'nwsTOOLTIP_ibfk_1' FOREIGN KEY ('id_story') REFERENCES 'nwsSTORY' ('id')
    );
    """
    __tablename__ = 'nwsTOOLTIP'

    id = db.Column(db.Integer(11), nullable=False, primary_key=True, autoincrement=True)
    id_story = db.Column(db.Integer(11), db.ForeignKey(nwsSTORY.id))
    body = db.Column(db.String(512), nullable=False)
    target_element = db.Column(db.String(256), nullable=False, default='')
    target_page = db.Column(db.String(256), nullable=False, default='')

    idstory = db.relationship('nwsSTORY', foreign_keys='nwsTOOLTIP.id_story')


#FUNCTIONS(VIEWS)

def get_latest_story_id():
    """
    SELECT id
    FROM nwsSTORY
    WHERE created >= DATE_SUB(CURDATE(),INTERVAL CFG_WEBNEWS_TOOLTIPS_COOKIE_LONGEVITY DAY)
    ORDER_BY created DESC LIMIT 1
    """

    result = connection.execute(select(nwsSTORY.id).
                             where(nwsSTORY.created >= datetime.now() - timedelta(days=CFG_WEBNEWS_TOOLTIPS_COOKIE_LONGEVITY)).
                             order_by(nwsSTORY.created.desc()).limit(1))

    if result:
        return result[0][0]
    return None

def get_story_tooltips(story_id):
    """
    SELECT id, body, target_element, target_page FROM nwsTOOLTIP WHERE id_story=story_id
    """
    result = connection.execute(select([nwsTOOLTIP.id, nwsTOOLTIP.target_element, nwsTOOLTIP.target_page]).where(nwsTOOLTIP.id_story == story_id))
    if result:
        return result
    return None

def update_tooltip(story_id,
                   tooltip_id,
                   tooltip_body,
                   tooltip_target_element,
                   tooltip_target_page,
                   is_tooltip_target_xpath = False):
    """
    UPDATE nwsTOOLTIP
    SET body=tooltip_body, target_element=tooltip_target_element, target_page=tooltip_target_page
    WHERE id=tooltip_id
    AND id_story=story_id
    """
    tooltip_target_element = is_tooltip_target_xpath and \
                             convert_xpath_expression_to_jquery_selector(tooltip_target_element) or \
                             tooltip_target_element

    result = connection.execute(update(nwsTOOLTIP.body, nwsTOOLTIP.target_element, nwsTOOLTIP.target_page).
                             values(tooltip_body, tooltip_target_element, tooltip_target_page).
                             where(nwsTOOLTIP.id==tooltip_id, nwsTOOLTIP.id_story==story_id))
    return result