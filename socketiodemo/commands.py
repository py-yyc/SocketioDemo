# -*- coding: utf-8 -*-
"""
Commands for controlling the AMS Cloud server instance.
"""
from flask_script import Command
from flask import current_app


# ---------------------------------------------------------------------------------------------------------
# WSGI SERVER
# ---------------------------------------------------------------------------------------------------------
class RunCommand(Command):
    """
    Starts the web server
    """

    def run(self):
        """
        Run the server
        """
        # noinspection PyProtectedMember
        app = current_app._get_current_object()  # Real app, not just the LocalProxy

        # Extract the stream extension we've bound to the app
        server = app.extensions['socketio']

        # Get config
        debug = app.config['DEBUG']
        listen_ip = app.config['IP']
        port = app.config['PORT']

        app.logger.info("Running on port %s", port)
        try:
            server.run(app, host=listen_ip, port=port, debug=debug)
        except (SystemExit, KeyboardInterrupt):
            app.logger.info("Stopping on port %s", port)
