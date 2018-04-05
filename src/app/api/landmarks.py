import sys
from flask import jsonify, request
from app.extensions import db, limiter
from app.models import Landmark
from app.api import api
from app.api.errors import bad_request
from sqlalchemy import func


@api.after_request
def add_header(response):
    response.cache_control.max_age = 60
    return response


@api.route('/boroughs/<int:boroughId>/landmarks', defaults={'search_query': None}, methods=['GET'])
@limiter.limit("100/day;20/hour;10/minute")
def get_landmarks(boroughId, search_query):
    search_query = request.args.get('search_query')
    landmark_query = Landmark.query.filter(Landmark.borough_id == boroughId)
    if search_query:
        landmark_query = \
            landmark_query.filter(func.lower(Landmark.name).contains(func.lower(search_query)) |
                                  func.lower(Landmark.description).contains(func.lower(search_query)) |
                                  func.lower(Landmark.date_designated).contains(func.lower(search_query)))

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Landmark.to_collection_dict(landmark_query, page, per_page,
                                       'api.get_landmarks', boroughId=boroughId)
    return jsonify(data)


@api.route('/boroughs/<int:boroughId>/landmarks/<int:id>', methods=['GET'])
def get_landmark(boroughId, id):
    landmark = Landmark.query \
        .filter(Landmark.borough_id == boroughId, Landmark.id == id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Landmark.to_collection_dict(landmark, page, per_page,
                                       'api.get_landmark', boroughId=boroughId, id=id)
    return jsonify(data)


@api.route('/boroughs/<int:boroughId>/landmarks', methods=['POST'])
def create_landmark(boroughId):
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data:
        return bad_request('must include name and description')
    landmark = Landmark()
    landmark.from_dict(data)
    landmark.borough_id = boroughId
    db.session.add(landmark)
    db.session.commit()
    return jsonify(landmark.to_dict()), 201


@api.route('/boroughs/<int:boroughId>/landmarks/<int:id>', methods=['PUT'])
def update_landmark(boroughId, id):
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data:
        return bad_request('must include name and description')
    landmark = Landmark.query \
        .filter(Landmark.borough_id == boroughId, Landmark.id == id) \
        .first_or_404()
    landmark.from_dict(data)
    db.session.commit()
    return '', 204


@api.route('/boroughs/<int:boroughId>/landmarks/<int:id>', methods=['PATCH'])
def partial_update_landmark(boroughId, id):
    landmark = Landmark.query \
        .filter(Landmark.borough_id == boroughId, Landmark.id == id) \
        .first_or_404()
    landmark.from_dict(request.get_json() or {})
    db.session.commit()
    return '', 204


@api.route('/boroughs/<int:boroughId>/landmarks/<int:id>', methods=['DELETE'])
def delete_landmark(boroughId, id):
    landmark = Landmark.query \
        .filter(Landmark.borough_id == boroughId, Landmark.id == id) \
        .first_or_404()
    db.session.delete(landmark)
    db.session.commit()
    return '', 204
