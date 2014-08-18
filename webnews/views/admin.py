# -*- coding: utf-8 -*-

"""nwsToolTip Flask Blueprint"""
from flask import Flask
from flask.ext.login import login_required
from flask import request, url_for, g, Markup, redirect, flash,Blueprint,render_template,current_app
from flask.ext import menu
from ..models import  NwsToolTip,NwsSTORY,NwsTAG
from flask.ext.menu import register_menu
from sqlalchemy.exc import IntegrityError
from invenio.ext.sqlalchemy import db
from werkzeug.debug import DebuggedApplication
from .. import config
blueprint = Blueprint('webnew_admin', __name__, template_folder='../templates',static_folder='../static' )
#@register_menu(blueprint, 'nwsToolTip', _('Search'), order=1)



@blueprint.route('/webnew_admin/admin')
@register_menu(blueprint, 'main.webnew.webnew_admin',config.CFG_WEBNEW_ADMIN_NAV_NAME,order=1)
def webnew_admin():
	  return render_template('admin.html',FormHeader='News Stories',visibility_story='block',visibility_tooltip='hidden')
@blueprint.route('/webnew_addRecord', methods=['GET', 'POST'])
def webnew_addRecord():
    stid=0
    if request.method == 'POST':
        try:
	    new_tooltip = NwsToolTip(body=str(request.form.get('txtBody_tooltip',None)),
                                     target_element=str(request.form.get('txttarget_element',None)),
                                     target_page=str(request.form.get('txttarget_page',None)))
            new_story = NwsSTORY(title=str(request.form.get('txtTitle',None)),body=str(request.form.get('txtBody_news',None)),nwsToolTip=[new_tooltip])
	    #new_story.nwsToolTip.append(new_tooltip)
	    db.session.add(new_story)
	    db.session.add(new_tooltip)
	    db.session.commit()
	    flash(config.CFG_WEBNEW_SUCCESS_RECORD_ADDED)
	    alert=config.CFG_WEBNEW_SUCCESS_ALERT
	    stid=new_story.id
        except IntegrityError, e:
            flash('Error')
	    alert=config.CFG_WEBNEW_ERROR_ALERT
        #return redirect(url_for('users'))
	return  render_template('admin.html',alert=alert,storyID=stid,FormHeader='ToolTip',visibility_story='hidden',visibility_tooltip='block')
    else:
        stories = User.query.all()
        return render_template('admin.html')

@blueprint.route('/webnew_addToolTip', methods=['GET', 'POST'])
def webnew_addToolTip():
    if request.method == 'POST':
        try:
            new_tooltip = NwsToolTip(id_story=21,
                                     body=str(request.form.get('txtBody',None)),
                                     target_element=str(request.form.get('txttarget_element',None)),
                                     target_page=str(request.form.get('txttarget_page',None)))
            db.session.add(new_tooltip)
            db.session.commit()
	    flash(config.CFG_WEBNEW_SUCCESS_RECORD_ADDED)
	    alert=config.CFG_WEBNEW_SUCCESS_ALERT
        except IntegrityError, e:
            flash('Error')
	    alert=config.CFG_WEBNEW_ERROR_ALERT
        #return redirect(url_for('users'))
	return  render_template('admin.html',alert=alert,visibility_story='hidden',visibility_tooltip='hidden')
    else:
        return render_template('admin.html')

#For Flask Menu

#@blueprint.route('/flaskmenu')
#@menu.register_menu(blueprint, '.', 'Home')
#def menuFlask():
  #  pass
#@blueprint.route('/')
#def FirstLoad_index():
    #return redirect(url_for('nwsToolTip.search_index'))
