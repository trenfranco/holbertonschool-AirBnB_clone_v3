#!/usr/bin/python3
"""amenity object data view API RESTful"""

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
def list_places(city_id):
    """returns all places using GET"""
    pl = []
    city = storage.get(City, city_id)
    if not city:
        aport(404)
    for a in city.places:
        pl.append(a.to_dict())
    return jsonify(pl)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def list_place(place_id):
    """returns a specific place using GET"""
    a = storage.get(Place, place_id)
    if not a:
        abort(404)
    return jsonify(a.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a place using DELETE"""
    a = storage.get(Place, place_id)
    if not a:
        abort(404)
    storage.delete(a)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """creates a place using POST"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    info = request.get_json()
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    info['city_id'] = city_id
    d = Place(**info)
    d.save()
    return make_response(jsonify(d.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates place using PUT"""
    a = storage.get(Place, place_id)
    if not a:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for k, v in info.items():
        if k not in ignore:
            setattr(a, k, v)
    storage.save()
    return make_response(jsonify(a.to_dict()), 200)
