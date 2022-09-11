#!/usr/bin/python3
"""amenity object data view API RESTful"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """returns all amenities using GET"""
    l = []
    amen = storage.all(Amenity).values()
    for a in amen:
        l.append(a.to_dict())
    return jsonify(l)


@app_views.route('/amenities/<amenity_id>/',
                 methods=['GET'], strict_slashes=False)
def list_amenity(amenity_id):
    """returns a specific amenity using GET"""
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    return jsonify(a.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a amenity using DELETE"""
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    storage.delete(a)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a amenity using POST"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    info = request.get_json()
    d = Amenity(**info)
    d.save()
    return make_response(jsonify(d.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates a ameni using PUT"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    info = request.get_json()
    for k, v in info.items():
        if k not in ignore:
            setattr(a, k, v)
    storage.save()
    return make_response(jsonify(a.to_dict()), 200)
