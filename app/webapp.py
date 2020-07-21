


from app.data.models import db

from app.controllers import indexes_api
from app.controllers import operation_api
from app.controllers import performance_api
from app.controllers import portfolio_api


import os

import logging

from flask import Flask, jsonify, redirect, make_response

#from flask_httpauth import HTTPBasicAuth # FUTURE


## config logs

logging.basicConfig(
            format='%(levelname)s: %(asctime)s - %(name)s - %(message)s', 
            #datefmt='%d/%m/%Y %H:%M:%S',
            level=logging.ERROR)

#logging.getLogger('werkzeug').setLevel(logging.INFO) # flask
#logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG) 

logging.getLogger('quote_current_bovespa_bvbmf').setLevel(logging.INFO) 
logging.getLogger('quote_current_bovespa_easynv').setLevel(logging.INFO) 
logging.getLogger('quote_current_crypto_foxbit').setLevel(logging.INFO) 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 




## config flask

app = Flask(__name__)


db_file = os.path.abspath(os.environ['INVEST_MONITOR_DB'] if 'INVEST_MONITOR_DB' in os.environ else 'demo.db')

if not os.path.exists(db_file):
    print('ERROR: '+db_file+' does not exist!')
    quit()
    
logger.info('DB: '+db_file)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+db_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # suppress warning

db.init_app(app)




# app routes

@app.route('/')
def root():
    return redirect('/static/')

@app.route('/static/')
def init_page():
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#@app.after_request
#def after_request(response):
#    response.headers['Access-Control-Allow-Origin'] = '*'
#    return response






app.register_blueprint(indexes_api.blueprint, url_prefix="/api/indexes")
app.register_blueprint(operation_api.blueprint, url_prefix="/api/operation")
app.register_blueprint(performance_api.blueprint, url_prefix="/api/performance")
app.register_blueprint(portfolio_api.blueprint, url_prefix="/api/portfolio")

