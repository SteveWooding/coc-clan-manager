"""Defines the views to be presented to the user."""
from flask import make_response, send_file

from cocman import app
from cocman.update_database import update_database

@app.route('/')
def index():
    if app.debug:
        return make_response(open('index.html').read())
    else:
        return send_file('index.html')


@app.route('/update/<update_key>/')
def update(update_key):
    """Update the database, given the update key.

    This is meant to be run on the server via curl and a cron job. The key
    protects against an outside source from updating the database, which may
    cause us to exceed CoC API limits.

    Example of curl command to run as a cron job:

        curl localhost/update/<update_key>/

    Args:
        update_key (str): Required key to actually perform the database update.

    """

    # Check the provided key is the correct one
    if update_key != app.config['UPDATE_KEY']:
        return 'Internal server error.\n', 500

    # Update the default clan
    update_database(app.config['MAIN_CLAN_TAG'])

    return 'OK!\n', 200
