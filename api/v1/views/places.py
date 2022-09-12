#!/usr/bin/python3
"""view for places objects API REST"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def retrunss_places(city_id):
    """return all plces in city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def return_place(place_id):
    """returns one place"""
    x = storage.get(Place, place_id)
    if not x:
        abort(404)
    return jsonify(x.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_placee(place_id):
    """deletes place"""
    x = storage.get(Place, place_id)
    if not x:
        abort(404)
    storage.delete(x)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def createee_place(city_id):
    """creates place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    placeInfo = request.get_json()
    user = storage.get(User, placeInfo['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    placeInfo["city_id"] = city_id
    data = Place(**placeInfo)
    data.save()
    return make_response(jsonify(data.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatee_place(place_id):
    """updates place"""
    x = storage.get(Place, place_id)
    if not x:
        abort(404)
    placeInfo = request.get_json()
    if not placeInfo:
        abort(400, description="Not a JSON")
    ignoredKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in placeInfo.items():
        if key not in ignoredKeys:
            setattr(x, key, value)
    storage.save()
    return make_response(jsonify(x.to_dict()), 200)
