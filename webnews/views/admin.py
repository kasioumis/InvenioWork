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

@blueprint.route('/admin/news')
@register_menu(blueprint, 'main.webnew.webnew_admin',config.CFG_WEBNEW_ADMIN_NAV_NAME,order=1)
def webnew_admin():
	  return render_template('admin.html',FormHeader='News Stories',visibility_story='block')
@blueprint.route('/admin/addrecord', methods=['GET', 'POST'])
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
                                 nwsToolTip=[new_tooltip],nwsTAG=[new_tag])
	    db.session.add(new_story)
	    db.session.add(new_tooltip)
	    db.session.add(new_story)
	    db.session.commit()
	    flash(config.CFG_WEBNEW_SUCCESS_RECORD_ADDED)
	    alert=config.CFG_WEBNEW_SUCCESS_ALERT
	    stid=new_story.id
        except IntegrityError, e:
            flash('Error')
	    alert=config.CFG_WEBNEW_ERROR_ALERT
        #return redirect(url_for('users'))
	return  render_template('admin.html',alert=alert,storyID=stid,FormHeader='ToolTip',visibility_story='hidden')
    else:
        stories = User.query.all()
        return render_template('admin.html')
