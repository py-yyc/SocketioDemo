# -*- coding: utf-8 -*-
"""
All routes for the HTML UI Representation
"""
from flask import Blueprint, request, render_template

from .constants import PRODUCT_NAME

ui_blueprint = Blueprint('ui', __name__)


@ui_blueprint.route('/')
@ui_blueprint.route('/echo')
def echo():
    """
    Show the route index
    """
    return render_template(
        'echo.html',
        path=request.path,
        product_name=PRODUCT_NAME
    )


@ui_blueprint.route('/rooms')
def rooms():
    """
    Show the route index
    """
    return render_template(
        'rooms.html',
        path=request.path,
        product_name=PRODUCT_NAME
    )