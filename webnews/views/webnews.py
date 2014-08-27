# -*- coding: utf-8 -*-

"""nwsToolTip Flask Blueprint"""
from flask import Flask
from flask.ext.login import login_required
from flask import request, url_for, g, Markup, redirect, flash,Blueprint,render_template,jsonify
from flask.ext import menu
from ..models import  NwsToolTip,NwsSTORY,NwsTAG
from flask.ext.menu import register_menu
from sqlalchemy.exc import IntegrityError
from werkzeug.debug import DebuggedApplication
from .. import config

blueprint = Blueprint('webnews', __name__, template_folder='../templates',static_folder='../static' )
#@register_menu(blueprint, 'main.webnews',config.CFG_WEBNEWS_ADMIN_MAIN_NAV)
#@register_menu(blueprint, 'webnews',config.CFG_WEBNEWS_ADMIN_MAIN_NAV)


@blueprint.route('/news')
@register_menu(blueprint, 'webnews.menu.search',[config.CFG_WEBNEWS_SEARCH_NAV_NAME,'glyphicon glyphicon-search','general'])
def search_index():
    result = NwsSTORY.query.filter_by(document_status='SHOW').limit(5).all()
    return render_template('search.html',searchResult=result)


@blueprint.route('/webnews/do_search', methods=['GET', 'POST'])
def do_search():
	 if request.method == 'POST':
		result = NwsSTORY.query.filter(NwsSTORY.title.contains(request.form['keywords']) | NwsSTORY.body.contains(request.form['keywords'])).filter_by(document_status='SHOW').all()
		return render_template('search.html',searchResult=result,resultshow='block')


@blueprint.route('/webnews/search/<RecordID>')
def search_detailindex(RecordID):
     try:
         result = NwsSTORY.query.get(RecordID)
         if result.document_status=='SHOW':
             return render_template('storyDetail.html',searchResult=result)
         else:
             return 'Not allowed'
     except:
          return 'Not allowed'


@blueprint.route('/show_tooltips')
def show_tooltips():
    targetpage = request.args.get('targetpage', 0, type=str)
    result1 = NwsToolTip.query.filter_by(target_page=targetpage).all()
    return jsonify(tooltip=[i.serialize for i in result1])