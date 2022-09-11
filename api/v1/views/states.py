#!/usr/bin/python3
"""state object data view API RESTful"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def list_states(state_id=None):
    """returns a state or all using GET"""
    if state_id is not None:
        state_list = storage.get(State, state_id)
        if not state_list:
            abort(404)
        return jsonify(state_list.to_dict())
    else:
        states = storage.all(State).values()
        states_list = []
        for i in states:
            states_list.append(i.to_dict())
        return jsonify(states_list)


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a state using DELETE"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a state using POST"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    state = request.json
    d = State(**state)
    d.save()
    return make_response(jsonify(d.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state using PUT"""
    if not request.json:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    info = request.json
    for k, v in info.items():
        if k not in ignore:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
