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
from invenio.ext.sqlalchemy import db
from .. import config


blueprint = Blueprint('webnewsadmin', __name__, template_folder='../templates',static_folder='../static' )
@register_menu(blueprint, 'main.webnewsadmin',config.CFG_WEBNEWS_ADMIN_NAV_NAME)


@blueprint.route('/webnews/Insert')
@register_menu(blueprint, 'main.webnewsadmin.Insert',config.CFG_WEBNEWS_ADMIN_INSERT)
def admin_Insert():
    return render_template('admin.html',FormHeader='News Stories',visibility_story='block',searchResult=0)
@blueprint.route('/webnews/addrecord', methods=['GET', 'POST'])
def webnew_addRecord():
    stid=0
    if request.method == 'POST':
        try:
            new_tooltip = NwsToolTip(body=str(request.form.get('txtBody_tooltip',None)),
                                     target_element=str(request.form.get('txttarget_element',None)),
                                     target_page=str(request.form.get('txttarget_page',None)))
            new_tag = NwsTAG(tag=str(request.form.get('txttag',None)))
            new_story = NwsSTORY(title=str(request.form.get('txtTitle',None)),
                                 body=str(request.form.get('txtBody_news',None)),
                                 document_status=str(request.form.get('st_document_status',None)),
                                 nwsToolTip=[new_tooltip],nwsTAG=[new_tag])
            db.session.add(new_story)
            db.session.add(new_tooltip)
            db.session.add(new_story)
            db.session.commit()
            flash(config.CFG_WEBNEWS_SUCCESS_RECORD_ADDED)
            alert=config.CFG_WEBNEWS_SUCCESS_ALERT
            stid=new_story.id
        except IntegrityError, e:
            flash('Error')
            alert=config.CFG_WEBNEWS_ERROR_ALERT
        #return redirect(url_for('users'))
	return  render_template('admin.html',alert=alert,storyID=stid,FormHeader='ToolTip',visibility_story='hidden')
    else:
        stories = NwsToolTip.query.all()
        return render_template('admin.html')


@blueprint.route('/webnews/updateRec', methods=['GET', 'POST'])
def webnew_updateRecord():

    stid=0
    if request.method == 'POST':
        try:
            id = str(request.form.get('news_ID',None))
            new_story=NwsSTORY.query.get(id)
            new_story.title=str(request.form.get('story_txtTitle',None))
            new_story.body=str(request.form.get('story_txtBody',None))
            new_story.document_status=str(request.form.get('story_docStatus',None))
            db.session.commit()
            new_tooltip=NwsToolTip.query.filter_by(id_story=id).first()
            new_tooltip.body=str(request.form.get('tooltip_txtBody',None))
            new_tooltip.target_element=str(request.form.get('tooltip_targetElement',None))
            new_tooltip.target_page=str(request.form.get('tooltip_targetPage',None))
            db.session.commit()
            new_tag=NwsTAG.query.filter_by(id_story=id).first()
            new_tag.tag=str(request.form.get('tag',None))


            db.session.commit()
            flash(config.CFG_WEBNEWS_SUCCESS_RECORD_ADDED)
            alert=config.CFG_WEBNEWS_SUCCESS_ALERT
            stid=new_story.id
            return  render_template('update.html',alert=alert,storyID=stid,FormHeader='ToolTip',visibility_story='hidden')
        except:
            result = NwsSTORY.query.order_by(NwsSTORY.id.desc()).limit(config.CFG_WEBNEWS_ADMIN_SHOWRECORDS).all()
            return render_template('Edit.html',searchResult=result,resultshow='block')
        #return redirect(url_for('users'))

    else:
        result = NwsSTORY.query.order_by(NwsSTORY.id.desc()).limit(config.CFG_WEBNEWS_ADMIN_SHOWRECORDS).all()
        return render_template('Edit.html',searchResult=result,resultshow='block')




@blueprint.route('/webnews/Edit')
@register_menu(blueprint, 'main.webnewsadmin.Edit',config.CFG_WEBNEWS_ADMIN_EDIT)
def admin_Edit():
    result = NwsSTORY.query.order_by(NwsSTORY.id.desc()).limit(config.CFG_WEBNEWS_ADMIN_SHOWRECORDS).all()
    return render_template('Edit.html',searchResult=result,resultshow='block')
    
    
@blueprint.route('/webnews/Update')
def admin_Update():
    try:
        id = request.args.get('id', None)
        result = NwsSTORY.query.get(id)
        return render_template('update.html',searchResult=result,News_ID=id)
    except:
        result = NwsSTORY.query.order_by(NwsSTORY.id.desc()).limit(config.CFG_WEBNEWS_ADMIN_SHOWRECORDS).all()
        return render_template('Edit.html',searchResult=result,resultshow='block')


@blueprint.route('/webnews/Delete')
def admin_Delete():
    try:
        id = request.args.get('id', None)

        new_story=NwsSTORY.query.get(id)
        new_tooltip=NwsToolTip.query.filter_by(id_story=id).first()
        new_tag=NwsTAG.query.filter_by(id_story=id).first()
        db.session.delete(new_tag)
        db.session.delete(new_tooltip)
        db.session.delete(new_story)
        db.session.commit()
        result = NwsSTORY.query.order_by(NwsSTORY.id.desc()).limit(config.CFG_WEBNEWS_ADMIN_SHOWRECORDS).all()
        return render_template('Edit.html',searchResult=result,resultshow='block')
    except:
        result = NwsSTORY.query.order_by(NwsSTORY.id.desc()).limit(config.CFG_WEBNEWS_ADMIN_SHOWRECORDS).all()
        return render_template('Edit.html',searchResult=result,resultshow='block')
