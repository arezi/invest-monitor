
from flask import Blueprint, jsonify


from app.data.models import Planning




blueprint = Blueprint("planning", __name__)





@blueprint.route('/', methods=['GET'])
def all():
    all = Planning.query.all()
    return jsonify([o.serialize() for o in all])


