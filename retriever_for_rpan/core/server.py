"""
This module defines a server which runs the Flask app on localhost, so it can interpret reddit's callbacks.
"""

from waitress import serve

from core.flaskapp import app


def run():
    """
    Starts a waitress server on localhost.
    """
    serve(app, host='0.0.0.0', port=65010, _quiet=True)
