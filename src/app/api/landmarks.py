import sys
from flask import jsonify, request
from app import db
from app.models import Landmark
from app.api import api
from app.api.errors import bad_request
from sqlalchemy import func


@api.route('/cities/<int:cityId>/landmarks', defaults={'search_query': None}, methods=['GET'])
def get_landmarks(cityId, search_query):
    search_query = request.args.get('search_query')
    landmark_query = Landmark.query.filter(Landmark.city_id == cityId)

    if search_query:
        landmark_query = \
        landmark_query.filter(func.lower(Landmark.name).contains(func.lower(search_query)) | \
                              func.lower(Landmark.description).contains(func.lower(search_query)))

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Landmark.to_collection_dict(landmark_query, page, per_page,
                                   'api.get_landmarks', cityId=cityId)
    return jsonify(data)


@api.route('/cities/<int:cityId>/landmarks/<int:id>', methods=['GET'])
def get_landmark(cityId, id):
    landmark = Landmark.query \
            .filter(Landmark.city_id == cityId, Landmark.id == id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Landmark.to_collection_dict(landmark, page, per_page,
                                       'api.get_landmark', cityId=cityId, id=id)
    return jsonify(data)


@api.route('/cities/<int:cityId>/landmarks', methods=['POST'])
def create_landmark(cityId):
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data:
        return bad_request('must include name and description fields')
    landmark = Landmark()
    landmark.from_dict(data)
    landmark.city_id = cityId
    db.session.add(landmark)
    db.session.commit()
    return jsonify(landmark.to_dict()), 201


@api.route('/cities/<int:cityId>/landmarks/<int:id>', methods=['PUT'])
def update_landmark(cityId, id):
    landmark = Landmark.query \
            .filter(Landmark.city_id == cityId, Landmark.id == id) \
            .first_or_404()
    landmark.from_dict(request.get_json() or {})
    db.session.commit()
    return '', 204


@api.route('/cities/<int:cityId>/landmarks/<int:id>', methods=['DELETE'])
def delete_landmark(cityId, id):
    landmark = Landmark.query \
            .filter(Landmark.city_id == cityId, Landmark.id == id) \
            .first_or_404()
    db.session.delete(landmark)
    db.session.commit()
    return '', 204
