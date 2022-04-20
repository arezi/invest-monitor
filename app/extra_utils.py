
'''
 utils for externals customers (like scripts and another applications that use services and repositories from this app)
'''

import os
from app.data.models import db
from flask import Flask

def init_db(db_file = os.environ['INVEST_MONITOR_DB']):

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+db_file
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # suppress warning

    db.init_app(app)
    app.app_context().push()

