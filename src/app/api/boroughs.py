from flask import jsonify, request
from app.extensions import db, limiter
from app.models import Borough
from app.api import api
from app.api.errors import bad_request
from sqlalchemy import func


@api.after_request
def add_header(response):
    response.cache_control.max_age = 60
    return response


@api.route('/boroughs', defaults={'search_query': None, 'order_by': None}, methods=['GET'])
@limiter.limit("100/day;10/hour;1/minute")
def get_boroughs(search_query, order_by):
    search_query = request.args.get('search_query')
    order_by = request.args.get('order_by')
    borough_query = Borough.query

    if search_query:
        borough_query = \
            borough_query.filter(func.lower(
                Borough.name).contains(func.lower(search_query)))

    if order_by == 'name':
        borough_query = borough_query.order_by('name')

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Borough.to_collection_dict(borough_query, page, per_page,
                                      'api.get_boroughs')
    return jsonify(data), 200


@api.route('/boroughs/<int:id>', methods=['GET'])
def get_borough(id):
    data = Borough.query.get_or_404(id).to_dict()
    return jsonify(data), 200


@api.route('/boroughs', methods=['POST'])
def create_borough():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name')
    borough = Borough()
    borough.from_dict(data)
    db.session.add(borough)
    db.session.commit()
    return jsonify(borough.to_dict()), 201


@api.route('/boroughs/<int:id>', methods=['PUT'])
def update_borough(id):
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('must include name')
    borough = Borough.query.get_or_404(id)
    borough.from_dict(data)
    db.session.commit()
    return '', 204


@api.route('/boroughs/<int:id>', methods=['PATCH'])
def partial_update_borough(id):
    borough = Borough.query.get_or_404(id)
    borough.from_dict(request.get_json() or {})
    db.session.commit()
    return '', 204


@api.route('/boroughs/<int:id>', methods=['DELETE'])
def delete_borough(id):
    borough = Borough.query.get_or_404(id)
    db.session.delete(borough)
    db.session.commit()
    return '', 204
