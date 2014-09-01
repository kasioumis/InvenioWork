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
from ..encoder import Encode,Decode

blueprint = Blueprint('webnews', __name__, template_folder='../templates',static_folder='../static' )
#@register_menu(blueprint, 'main.webnews',config.CFG_WEBNEWS_ADMIN_MAIN_NAV)
#@register_menu(blueprint, 'webnews',config.CFG_WEBNEWS_ADMIN_MAIN_NAV)


@blueprint.route(config.CFG_WEBNEWS_MENU_INDEX)
@register_menu(blueprint, 'webnews.menu.search',[config.CFG_WEBNEWS_SEARCH_NAV_NAME,'glyphicon glyphicon-search','general'])
def index():
    result = NwsSTORY.query.filter_by(document_status='SHOW').limit(5).all()
    return render_template('search.html',searchResult=result ,EncodeStr=Encode)


@blueprint.route(config.CFG_WEBNEWS_SEARCH, methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            result = NwsSTORY.query.filter(NwsSTORY.title.contains(request.form['keywords']) | NwsSTORY.body.contains(request.form['keywords'])).filter_by(document_status='SHOW').all()
            return render_template('search.html',searchResult=result,resultshow='block' ,EncodeStr=Encode)
        except IntegrityError, e:
            flash('Error')
            alert=config.CFG_WEBNEWS_ERROR_ALERT
    try:
        keywords=Decode(request.args.get('keywords', Encode(None)))
        result1 = NwsTAG.query.filter(NwsTAG.tag.contains(keywords)).all()

        result = NwsSTORY.query.filter(NwsSTORY.id.in_(appendToListy(result1))).filter_by(document_status='SHOW').all()
        return render_template('search.html',searchResult=result,resultshow='block',EncodeStr=Encode)

    except IntegrityError, e:
        flash('Error')
        alert=config.CFG_WEBNEWS_ERROR_ALERT


@blueprint.route('/show_tooltips')
def show_tooltips():
    targetpage = request.args.get('targetpage', 0, type=str)
    result1 = NwsToolTip.query.filter((NwsToolTip.target_page==targetpage) | (NwsToolTip.target_page=='*') ).all()

    #filter((User.username == name) | (User.email == email))
    return jsonify(tooltip=[i.serialize for i in result1])

def appendToListy(object):
    Lst=[]
    for result in object:
        Lst.append(result.id_story)

    return Lst