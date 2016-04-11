"""Defines the views to be presented to the user."""
from flask import make_response, send_file

from cocman import app

@app.route('/')
def index():
    if app.debug:
        return make_response(open('index.html').read())
    else:
        return send_file('index.html')
