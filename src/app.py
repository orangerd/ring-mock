#!/usr/bin/python
"""Main entry point for the ring mock server."""

from flask import Flask
from flask import abort

APP = Flask(__name__)

import os.path

APP.config.update(
    DEBUG=True,
)

@APP.route('/doorbots_api/vod/ready')
def ready():
    abort(404)

if __name__ == '__main__':
    APP.run()
