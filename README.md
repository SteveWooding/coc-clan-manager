# coc-clan-manager
### by Steven Wooding
Clash of Clans Clan Manager web app

## What it is and does
This is a web app for collecting and analysing clan statistics. Its key feature
is the tracking of total troop donations over many seasons and tracking when
a member last donated troops.

The front-end is a simple AngularJS app, while the back-end is a Flask app
written in Python, with the data stored in an SQL database (SQLite in dev
environment, PostgreSQL for production).

## Required Libraries and Dependencies

The back-end requires Python 2.7.x and the following Python PIP packages:

* cffi==1.5.2
* coc==0.2
* cryptography==1.2.3
* enum34==1.1.2
* Flask==0.10.1
* idna==2.0
* ipaddress==1.0.16
* itsdangerous==0.24
* Jinja2==2.8
* MarkupSafe==0.23
* ndg-httpsclient==0.4.0
* psycopg2==2.6.1
* pyasn1==0.1.9
* pycparser==2.14
* pyOpenSSL==0.15.1
* requests==2.9.1
* six==1.10.0
* SQLAlchemy==1.0.12
* urllib3==1.14
* uWSGI==2.0.12
* Werkzeug==0.11.4

These can be installed within your Python environment using the
`requirements.txt` file in the root of the repository with:

```
pip install -r requirements.txt
```

The front-end requirements are loaded in from the web. These include:

* AngularJS 1.5.3
* jQuery 1.12.0
* Bootstrap 3.3.6

## Project contents

TODO

## Running the project
### Development mode
TODO

### Production deployment
TODO

## Contributions
Feedback and feature requests are welcome via Git Hub Issues. All Pull Requests
will be considered.
