# -*- coding: utf-8 -*-

"""nwsToolTip Flask Blueprint"""
from flask import Flask
from flask.ext.login import login_required
from flask import request, url_for, g, Markup, redirect, flash,Blueprint,render_template
from flask.ext import menu
from ..models import  NwsToolTip,NwsSTORY,NwsTAG
from flask.ext.menu import register_menu
from sqlalchemy.exc import IntegrityError
from werkzeug.debug import DebuggedApplication
from .. import config

blueprint = Blueprint('webnews', __name__, template_folder='../templates',static_folder='../static' )
@register_menu(blueprint, 'main.webnews',config.CFG_WEBNEWS_ADMIN_MAIN_NAV)
#@register_menu(blueprint, 'nwsToolTip', _('Search'), order=1)


@blueprint.route('/')
@register_menu(blueprint, 'main.webnews.search',config.CFG_WEBNEWS_SEARCH_NAV_NAME)
def search_index():
    return render_template('search.html',resultshow='hidden')

#@blueprint.route('/tooltip', methods=['GET', 'POST'])

#def index():
 #   tooltips = NwsToolTip.query.all()
  #  return render_template('index.html',tooltips=tooltips)

@blueprint.route('/do_search', methods=['GET', 'POST'])
def do_search():
	 if request.method == 'POST':
		result = NwsSTORY.query.filter(NwsSTORY.title.contains(request.form['keywords']) | NwsSTORY.body.contains(request.form['keywords'])).all()
		return render_template('search.html',searchResult=result,resultshow='block')



@blueprint.route('/webnew_admin/nav')

def webnew_nav():
	  return render_template('nav.html')

#For Flask Menu

#@blueprint.route('/flaskmenu')
#@menu.register_menu(blueprint, '.', 'Home')
#def menuFlask():
  #  pass
#@blueprint.route('/')
#def FirstLoad_index():
    #return redirect(url_for('nwsToolTip.search_index'))
