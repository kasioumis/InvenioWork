# -*- coding: utf-8 -*-

"""nwsToolTip Flask Blueprint"""
from flask import Flask
from flask import request, url_for, g, Markup, redirect, flash,Blueprint,render_template
from . models import  NwsToolTip

from sqlalchemy.exc import IntegrityError
from werkzeug.debug import DebuggedApplication

blueprint = Blueprint('nwsToolTip', __name__, template_folder='templates',static_folder='static' )


@blueprint.route('/tooltip', methods=['GET', 'POST'])
def index():
    tooltips = NwsToolTip.query.all()
    return render_template('index.html',tooltips=tooltips)

