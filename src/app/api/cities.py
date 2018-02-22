from flask import jsonify, request
from app import db
from app.models import City
from app.api import api
from app.api.errors import bad_request
from sqlalchemy import func


@api.route('/cities', defaults={'search_query': None, 'order_by': None}, methods=['GET'])
def get_cities(search_query, order_by):
    search_query = request.args.get('search_query')
    order_by = request.args.get('order_by')
    city_query = City.query

    if search_query:
        city_query = \
        city_query.filter(func.lower(City.name).contains(func.lower(search_query)) | \
                          func.lower(City.state).contains(func.lower(search_query)))

    if order_by == 'name':
        city_query = city_query.order_by('name')

    if order_by == 'state':
        city_query = city_query.order_by('state')

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = City.to_collection_dict(city_query, page, per_page,
                                   'api.get_cities')
    return jsonify(data), 200


@api.route('/cities/<int:id>', methods=['GET'])
def get_city(id):
    data = City.query.get_or_404(id).to_dict()
    return jsonify(data), 200


@api.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json() or {}
    if 'name' not in data or 'state' not in data:
        return bad_request('must include name and state fields')
    city = City()
    city.from_dict(data)
    db.session.add(city)
    db.session.commit()
    return jsonify(city.to_dict()), 201


@api.route('/cities/<int:id>', methods=['PUT'])
def update_city(id):
    city = City.query.get_or_404(id)
    city.from_dict(request.get_json() or {})
    db.session.commit()
    return '', 204


@api.route('/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    city = City.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    return '', 204
