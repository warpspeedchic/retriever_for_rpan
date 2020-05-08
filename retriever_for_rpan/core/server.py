from waitress import serve

from core.flaskapp import app


def run():
    serve(app, host='0.0.0.0', port=65010, _quiet=True)
