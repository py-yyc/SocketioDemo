#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Must be first
from gevent.monkey import patch_all
patch_all()

import os

from socketiodemo import create_app


def run_manager():
    """
    Create an application instance and run the application manager (for CLI interface).
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    configuration_file = os.path.join(dir_path, 'user_settings.cfg')
    app = create_app(configuration_file)
    # noinspection PyUnresolvedReferences
    app.cli()


if __name__ == '__main__':
    run_manager()

