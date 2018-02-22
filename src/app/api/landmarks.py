from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request
from app.api.errors import bad_request


@api.route('/cities/<int:cityId>/landmarks', methods=['GET'])
def get_landmarks(cityId):
    landmarks = Landmark.query \
            .filter_by(Landmark.city_id == cityId)
            .first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = City.to_collection_dict(landmark, page, per_page, 
                                      'api.get_cities')
    return jsonify(data)


@api.route('/cities/<int:cityId>/landmarks/<int:id>', methods=['GET'])
def get_landmark(cityId, id):
    landmark = Landmark.query \
            .filter(Landmark.city_id == cityId, Landmark.id == id)
            .get_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Landmark.to_collection_dict(landmark, page, per_page,
                                       'api.get_landmark', id=id)
    return jsonify(data)


@api.route('/cities/<int:cityId>/landmarks', methods=['POST'])
def create_landmark(cityId):
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data or 'cityId' not in data:
        return bad_request('must include name, description and cityId fields')
    landmark = Landmark()
    landmark.from_dict(data, new_user=True)
    db.session.add(landmark)
    db.session.commit()
    response = jsonify(landmark.to_dict())
    response.status_code = 201
    return response


@api.route('/cities/<int:cityId>/landmarks/<int:id>', methods=['PUT'])
def update_landmark(cityId, id):
    data = request.get_json() or {}
    landmark = Landmark()
    landmark = Landmark.query \
            .filter(Landmark.city_id == cityId, Landmark.id == id)
            .get_or_404()
    data = request.get_json() or {}
    landmark.from_dict(request.get_json() or {})
    db.session.commit()
    return '', 204


@api.route('/cities/<int:cityId>/landmarks/<int:id>', methods=['DELETE'])
def delete_landmark(cityId, id):
    landmark = Landmark.query \
            .filter(Landmark.city_id == cityId, Landmark.id == id)
            .get_or_404()
    db.session.delete(landmark)
    db.session.commit()
    return '', 204
