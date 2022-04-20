


from flask import Blueprint, jsonify

from app.services import portfolio_service



blueprint = Blueprint("portfolio", __name__)




@blueprint.route('/stocks', methods=['GET'])
def stocks():
    map_stocks = portfolio_service.get_stocks()
    return jsonify(list(map_stocks.keys()))


@blueprint.route('/quote', methods=['GET'])
def quote():
    return jsonify(portfolio_service.quote())


