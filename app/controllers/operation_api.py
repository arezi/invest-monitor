
from flask import Blueprint, jsonify


from app.data import operation_repository
from app.data.models import Operation




blueprint = Blueprint("operation", __name__)



@blueprint.route('/sold/<string:stocks_exchange>/current_month', methods=['GET'])
def sum_sold_current_month(stocks_exchange):
    return jsonify({stocks_exchange : operation_repository.sum_sold_current_month(stocks_exchange)})



@blueprint.route('/', methods=['GET'])
def all():
    all = Operation.query.all()
    return jsonify([o.serialize() for o in all])


