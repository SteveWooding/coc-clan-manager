#!/usr/bin/env python
"""Main script to start the CoC Clan Management app in development mode."""
import os.path

from cocman import app
from cocman.database_setup import create_db
from cocman.update_database import update_database

if __name__ == '__main__':
    # App configuration
    app.config['DATABASE_URL'] = 'sqlite:///cocman.db'
    app.config['COC_API_KEY'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImE2ZjVhYTZlLWZlOWMtNDY1OS1hOWZkLWE2YjVmYWEyNTZiMiIsImlhdCI6MTQ1NzcxMTY5Niwic3ViIjoiZGV2ZWxvcGVyLzRiNmUyZWE0LWIwNmUtNDlmMy01MGI5LTk3MTFhMjc0ZDM5ZCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjgyLjI2LjEwNC41NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.-OTLoTXxvl714NAI12hRW9BpIZ8Sq8rjvXbnt5zZwb8q_nz_o4lGjMaOAzVSYuEJB4sw2oLyWheRWB-IJ8qIjg'
    app.config['MAIN_CLAN_TAG'] = '#28Y8YLLJ';
    app.config['UPDATE_KEY'] = 'devkey';  # Change this in production.

    if os.path.isfile('cocman.db') is False:
        create_db(app.config['DATABASE_URL'])

    update_database(app.config['MAIN_CLAN_TAG'])

    app.debug = True
    app.run(host='0.0.0.0', port=8000)
