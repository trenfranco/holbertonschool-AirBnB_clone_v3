#!/usr/bin/python3
"""last task added cors"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import environ


def not_found(self):
    """handles 404"""
    dic = {"error": "Not found"}
    return jsonify(dic), 404


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.register_error_handler(404, not_found)


@app.teardown_appcontext
def teadown(self):
    """manage teardown"""
    storage.close()

if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = environ.get('HBNB_API_PORT')
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
