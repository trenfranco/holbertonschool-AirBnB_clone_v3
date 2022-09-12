#!/usr/bin/python3
"""review objects RESTFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.review import Review
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def retrieve_reviews(place_id):
    """returns all revs in place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrieve_review(review_id):
    """returns review"""
    x = storage.get(Review, review_id)
    if not x:
        abort(404)
    return jsonify(x.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """deletes review"""
    x = storage.get(Review, review_id)
    if not x:
        abort(404)
    storage.delete(x)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """creates review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    info = request.get_json()
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    info["place_id"] = place_id
    data = Review(**info)
    data.save()
    return make_response(jsonify(data.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates review"""
    x = storage.get(Review, review_id)
    if not x:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, description="Not a JSON")
    ignoredKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in info.items():
        if key not in ignoredKeys:
            setattr(x, key, value)
    storage.save()
    return make_response(jsonify(x.to_dict()), 200)
