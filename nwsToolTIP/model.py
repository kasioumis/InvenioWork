from flask.ext.sqlalchemy import SQLAlchemy
 
SQLALCHEMY_DATABASE_URI= 'sqlite:///./test.db'
 
db = SQLAlchemy()
 
class NwsTOOLTIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_story = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String(256), nullable=False)
    target_element = db.Column(db.String(120), nullable=False)
    target_page = db.Column(db.String(256), nullable=False)
 
    def __init__(self, id_story, body,target_element,target_page):
   	print(id_story)
    	self.id_story = id_story
    	self.body = body
    	self.target_element = target_element
    	self.target_page = target_page
	
    def __repr__(self):
        return '<Target Page %r>' % self.target_page
 
    @classmethod
    def by_id(cls, id_story):
        return db.query(cls).filter(cls.id==id_story).first()
 
    @classmethod
    def by_target_page(cls, target_page):
        return db.query(cls).filter(cls.target_page==target_page).first()


def init_db(app):
    db.init_app(app)
    return app
