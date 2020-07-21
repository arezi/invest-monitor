


from flask import Blueprint, jsonify

from app.services import portfolio_service



blueprint = Blueprint("portfolio", __name__)





@blueprint.route('/quote', methods=['GET'])
def quote_portfolio():
    return jsonify(portfolio_service.quote())


