"""Initialisation for the cocman package."""
from flask import Flask

# Initialise the Flask app object
app = Flask(__name__)

# Import modules that have the route() decorator in them.
# OK to have circular imports here as they are not used in this file.
# Ref: http://flask.pocoo.org/docs/0.10/patterns/packages/
import cocman.views