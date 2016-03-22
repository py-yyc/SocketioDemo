# -*- coding: utf-8 -*-
"""
Flask application factory for a Flask-Socket.io Demo app
"""
from __future__ import absolute_import

from logging import INFO, DEBUG, StreamHandler

from flask import Flask
from flask_script import Manager
from flask_script.commands import Clean, ShowUrls

from . import settings
from .api import api_blueprint
from .commands import RunCommand
from .stream import create_stream
from .views import ui_blueprint


def create_app(configuration_file):
    """
    Create the app.

    :param configuration_file: Path of the configuration file to use for deployment settings
    :return: New application to use
    """
    # Setup the Flask app instance and configuration
    app = Flask(__name__)
    app.config.from_object(settings)  # Setup default settings
    app.config.from_pyfile(configuration_file, silent=True)  # Override with user settings -- and silence failures

    # Setup a little bit of console logging
    if app.config['DEBUG']:
        app.logger.setLevel(DEBUG)
    else:
        app.logger.setLevel(INFO)
        app.logger.addHandler(StreamHandler())

    manager = Manager(app)

    # Initialize the Socket.io Stream and bind it to the app instance (Only one stream per app at this time)
    async_mode = 'threading' if app.config['DEBUG'] else 'gevent'
    create_stream(app, resource='/api/v1/stream', async_mode=async_mode)

    # Add all Flask-Script manager commands
    manager.add_command('runserver', RunCommand)
    manager.add_command('clean', Clean)
    manager.add_command('urls', ShowUrls)

    # Create simple to use function on the app for starting commands
    # noinspection PyUnusedLocal
    def _cli(self):
        manager.run()
    # noinspection PyUnresolvedReferences
    app.cli = _cli.__get__(app, app.__class__)

    # Load all blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(ui_blueprint, url_prefix='')

    return app
