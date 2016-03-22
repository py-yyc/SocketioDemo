# -*- coding: utf-8 -*-
"""
All routes for the HTML UI Representation
"""
from flask import Blueprint, jsonify


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/')
def index():
    """
    Show the route index
    """
    response = {
        "message": "I'm an API!"
    }
    return jsonify(response)