#!/usr/bin/env python
"""Main Python script to start the CoC Clan Management app in development mode."""

from cocman import app

if __name__ == '__main__':
    # App configuration
    app.config['DATABASE_URL'] = 'sqlite:///cocman.db'

    if os.path.isfile('cocman.db') is False:
        create_db(app.config['DATABASE_URL'])
        update_database()

    app.debug = True
    app.run(host='0.0.0.0', port=8000)