# -*- coding: utf-8 -*-

"""nwsToolTip Flask Blueprint"""
from flask import Flask
from flask.ext.login import login_required
from flask import request, url_for, g, Markup, redirect, flash,Blueprint,render_template,jsonify, session
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
        id=int(Decode(request.args.get('id', Encode(0))))
        if keywords=='1':
           result1 = NwsSTORY.query.get(id)
           return render_template('details.html',searchResult=result1)
        result1 = NwsTAG.query.filter(NwsTAG.tag.contains(keywords)).all()
        result = NwsSTORY.query.filter(NwsSTORY.id.in_(appendToListy(result1))).filter_by(document_status='SHOW').all()
        return render_template('search.html',searchResult=result,resultshow='block',EncodeStr=Encode)

    except IntegrityError, e:
        flash('Error')
        alert=config.CFG_WEBNEWS_ERROR_ALERT


@blueprint.route('/show_tooltips')
def show_tooltips():
    targetpage = request.args.get('targetpage', 0, type=str)
    try:
        #session['exclude_ids']=[]
        #targetpage = request.args.get('targetpage', 0, type=str)
        if session['exclude_ids']:
            result1 = NwsToolTip.query.filter(((NwsToolTip.target_page==targetpage) | (NwsToolTip.target_page=='*')) & (NwsToolTip.target_element.notin_(excludeList(targetpage)))).all()
        else:
            result1 = NwsToolTip.query.filter((NwsToolTip.target_page==targetpage) | (NwsToolTip.target_page=='*')).all()
    except:
        session['exclude_ids']=[]
        result1 = NwsToolTip.query.filter((NwsToolTip.target_page==targetpage) | (NwsToolTip.target_page=='*')).all()


    #filter((User.username == name) | (User.email == email))


    return jsonify(tooltip=[i.serialize for i in result1])

def appendToListy(object):
    Lst=[]
    for result in object:
        Lst.append(result.id_story)
    return Lst

@blueprint.route('/tooltips_exclude')
def exclude_tooltip():
    targetpage = request.args.get('targetpage', 0, type=str)
    tooltipElement=request.args.get('tooltipElement', 0, type=str)
    SessionList=[]
    if session['exclude_ids']:
       SessionList= session['exclude_ids']
       if UniqueInsert(SessionList,tooltipElement,targetpage):
           SessionList.append({'page': targetpage, 'Element':tooltipElement })
           session['exclude_ids']=SessionList
    else:
        SessionList=[{'page': targetpage, 'Element':tooltipElement }]
        session['exclude_ids']=SessionList


    return jsonify(result='added')

def UniqueInsert(Obj,element, page):
    for item in Obj:
        if item['Element']== element and  item['page']==page:
            return False
    return True

def excludeList(page):
    Lst=[]
    if session['exclude_ids']:
        for item in session['exclude_ids']:
            if  item['page']==page:
                Lst.append(item['Element'])

    return Lst