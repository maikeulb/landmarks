from flask import jsonify, request, url_for
from app import db
from app.models import City
from app.api import api
from app.api.errors import bad_request


@api.route('/cities', methods=['GET'])
def get_cities():
    city_query = City.query
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = City.to_collection_dict(city_query, page, per_page, 
                                      'api.get_cities')
    return jsonify(data), 200


@api.route('/cities/<int:id>', methods=['GET'])
def get_city(id):
    data = City.query.get_or_404(id)
    return jsonify(data), 200


@api.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data or 'enrollment_date' not in data:
        return bad_request('must include first_name, last_name and \
                           enrollment_date fields')
    city = City()
    city.from_dict(data)
    db.session.add(city)
    db.session.commit()
    response = jsonify(city.to_dict())
    return response, 201


@api.route('/cities/<int:id>', methods=['PUT'])
def update_city(id):
    city = City.query.get_or_404(id)
    data = request.get_json() or {}
    city.from_dict(request.get_json() or {}, new_user=False)
    db.session.commit()
    response.status_code = 204
    return response


@api.route('/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    city = City.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    response.status_code = 204
    return response
