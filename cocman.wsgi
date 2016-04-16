#!/usr/bin/env python
"""WSGI script for app deployment in a production environment."""
from cocman import app as application
from cocman.database_setup import create_db
from cocman.update_database import update_database

application.config['DATABASE_URL'] = 'postgresql://cocman:password@localhost/cocman'
application.config ['COC_API_KEY'] = 'PleaseReplaceWithYourOwnApiKey'
application.config['MAIN_CLAN_TAG'] = '#28Y8YLLJ';  # Default clan to track
application.config['UPDATE_KEY'] = 'PleaseChangeMe';

# Create the database (if it does already exist) and update.
create_db(application.config['DATABASE_URL'])
update_database(application.config['MAIN_CLAN_TAG'])
