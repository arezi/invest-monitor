
from unittest import TestCase

from app.data.models import db

from flask import Flask


db_file = ':memory:'
#db_file = 'test3.db'


class AbstractTestRepository(TestCase):

    @classmethod
    def setUpClass(cls):
        global db_file

        if db_file == None:
            return

        #print('creating db schema')

        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+db_file
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # suppress warning

        db_file = None

        db.init_app(app)
        app.app_context().push()

        conn = db.session.connection().connection;
        cursor = conn.cursor()
        import os
        for file in os.listdir('../migrations'):
            with open(os.path.join('../migrations',file), 'rt') as f:
                sql = f.read()
            cursor.executescript(sql)

