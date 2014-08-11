# -*- coding: utf-8 -*-

"""nwsToolTip Flask Blueprint"""
from flask import Flask
from flask.ext.login import login_required
from flask import request, url_for, g, Markup, redirect, flash,Blueprint,render_template
from . models import  NwsToolTip,NwsSTORY
from sqlalchemy.exc import IntegrityError

from sqlalchemy.exc import IntegrityError
from werkzeug.debug import DebuggedApplication

blueprint = Blueprint('nwsToolTip', __name__, template_folder='templates',static_folder='static' )


@blueprint.route('/tooltip', methods=['GET', 'POST'])
def index():
    tooltips = NwsToolTip.query.all()
    return render_template('index.html',tooltips=tooltips)
@blueprint.route('/admin/search', methods=['GET', 'POST'])
def search_index():
    return render_template('search.html')
@blueprint.route('/do_search', methods=['GET', 'POST'])
def do_search():
	 if request.method == 'POST':
		result = NwsSTORY.query.filter(NwsSTORY.title.contains(request.form['keywords']) | NwsSTORY.body.contains(request.form['keywords'])).all()
		return render_template('result.html',searchResult=result)

@blueprint.route('/admin/news', methods=['GET', 'POST'])
def admin():
    #Return the form and the messages so far
    nwsTOOLTIP = NwsToolTip.query.all()
    return render_template('admin.html', tooltips=nwsTOOLTIP)


