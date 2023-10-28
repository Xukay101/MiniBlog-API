from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app import db

bp = Blueprint('posts', __name__)

class PostAPI(MethodView):

    def get(self, post_id):
        if post_id is None:
            # Return list of posts
            return jsonify(message='List of posts')
        else:
            # Return a single post
            return jsonify(message='Get post')

    def post(self):
        # Create a new post
        return jsonify(message='Create new Post')

    def delete(self, post_id):
        # Delete a single post
        return jsonify(message='Delete Post')

    def put(self, post_id):
        # Update a single post
        return jsonify(message='Update Post')

post_view = PostAPI.as_view('post_api')
bp.add_url_rule('/', defaults={'post_id': None}, view_func=post_view, methods=['GET',])
bp.add_url_rule('/', view_func=post_view, methods=['POST',])
bp.add_url_rule('/<int:post_id>/', view_func=post_view, methods=['GET', 'PUT', 'DELETE'])