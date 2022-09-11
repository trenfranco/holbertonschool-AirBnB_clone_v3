#!/usr/bin/python3
"""city object data view API RESTful"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    """returns all cities of a state using GET"""
    cities = []
    state_list = storage.get(State, state_id)
    if not state_list:
        abort(404)
    for city in state_list.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def list_city(city_id):
    """returns a specific city using GET"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city using DELETE"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates a state using POST"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    info = request.get_json()
    d = City(**info)
    d.state_id = state.id
    d.save()
    return make_response(jsonify(d.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state(city_id):
    """updates a city using PUT"""
    if not request.json:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    info = request.json
    for k, v in info.items():
        if k not in ignore:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
