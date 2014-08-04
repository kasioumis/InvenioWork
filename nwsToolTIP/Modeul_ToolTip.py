from flask import Flask
from flask import request, url_for, g, Markup, redirect, flash
from model import db, init_db, NwsTOOLTIP
 
from flask import render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.debug import DebuggedApplication
 
app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app)
app.secret_key = 'mysecret'
 
#SQLAlchemy integration
app.config.from_object('model')
app = init_db(app)
 
@app.before_first_request
def init():
    db.create_all()
 
@app.before_request
def before_request():
    g.db = db
 
@app.teardown_request
def close_connection(exception):
    pass
 
@app.route('/')
def index():
    return render_template('index.html')
 

@app.route('/nwsTOOLTIP',methods=['GET', 'POST'])
def nwsTOOLTIP():
    if request.method == 'POST':
        try:
            new_tooltip = NwsTOOLTIP(*request.form.values())
            db.session.add(new_tooltip)
            db.session.commit()
        except IntegrityError, e:
            flash("No ToolTip Added!!")
        return redirect(url_for('nwsTOOLTIP'))
    else:
        #Return the form and the messages so far
        nwsTOOLTIP = NwsTOOLTIP.query.all()
        return render_template('nwsTOOLTIP.html', nwsTOOLTIP=nwsTOOLTIP)
 
def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(host='127.0.0.3')
